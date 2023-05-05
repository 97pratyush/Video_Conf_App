#include "socketserver.h"
#include "QtWebSockets/qwebsocketserver.h"
#include "QtWebSockets/qwebsocket.h"
#include <QtCore/QDebug>
#include <iostream>
#include <memory>
#include <QJsonDocument>
#include <QJsonObject>
#include <QJsonArray>

SocketServer::SocketServer(quint16 port, bool debug, QObject *parent) : QObject(parent), webSocketServer(new QWebSocketServer(QStringLiteral("Socket Server"), QWebSocketServer::NonSecureMode, this))
{
    if(this->webSocketServer->listen(QHostAddress::Any, port)){
        qDebug() << "SocketServer listening on port" << port;
        connect(webSocketServer, SIGNAL(newConnection()), this, SLOT(onNewConnection()));
        //        connect(webSocketServer, &QWebSocketServer::newConnection, this, &SocketServer::closed);
    }else{
        throw std::runtime_error("SocketServer failed to listen");
    }
}

SocketServer::~SocketServer()
{
    webSocketServer->close();
    for (auto it = socketClients.begin(); it != socketClients.end(); ++it) {
        qDeleteAll(it.value());
    }
    socketClients.clear();}

void SocketServer::onNewConnection()
{
    try {
        QWebSocket *pSocket = webSocketServer->nextPendingConnection();
        qDebug() << "New Connection" << pSocket;
        connect(pSocket, &QWebSocket::textMessageReceived, this, &SocketServer::processTextMessage);
        connect(pSocket, &QWebSocket::disconnected, this, &SocketServer::socketDisconnected);
    } catch (...) {
        qDebug() << "Error:";

    }

}

void SocketServer::notifyParticipantListUpdated(QString& meetingId)
{

    // Get the list of participant user IDs for the given meeting ID
    QStringList participantList;
    QMap<QString, QWebSocket*> meetingParticipants = socketClients[meetingId];
    for (auto it = meetingParticipants.constBegin(); it != meetingParticipants.constEnd(); ++it) {
        participantList << it.key();
    }

    // Create a JSON message with the updated participant list
    QJsonObject messageObj;
    messageObj.insert("type", "participantListUpdated");
    messageObj.insert("meetingId", meetingId);
    messageObj.insert("participantList", QJsonArray::fromStringList(participantList));
    QJsonDocument messageDoc(messageObj);
    QString messageStr(messageDoc.toJson(QJsonDocument::Compact));

    // Send the message to each participant in the meeting
    for (auto it = meetingParticipants.constBegin(); it != meetingParticipants.constEnd(); ++it) {
        QWebSocket *participantSocket = it.value();
        if (participantSocket && participantSocket->isValid()) {
            participantSocket->sendTextMessage(messageStr);
        }
    }
    return;
}

void SocketServer::addAndNotifyChatMessage(QString meetingId, QString userName, QString message)
{
    QJsonObject messageObj;
    messageObj.insert("type", "newChatMessage");
    messageObj.insert("meetingId", meetingId);
    messageObj.insert("sender", userName);
    messageObj.insert("message", message);

    QJsonDocument messageDoc(messageObj);
    QString messageStr = QString::fromUtf8(messageDoc.toJson());

    if (chatHistory.contains(meetingId)) {
        QList<QPair<QString, QString>> messages = chatHistory.value(meetingId);
        messages.append(qMakePair(userName, message));
        chatHistory.insert(meetingId, messages);
    } else {
        QList<QPair<QString, QString>> messages;
        messages.append(qMakePair(userName, message));
        chatHistory.insert(meetingId, messages);
    }

    // Notify all clients subscribed to this meeting's chat
    if (socketClients.contains(meetingId) && socketClients[meetingId].size() > 0) {
        for (auto client = socketClients[meetingId].begin(); client != socketClients[meetingId].end(); ++client) {
            if (client.value()->isValid() && client.value()->state() == QAbstractSocket::ConnectedState) {
                client.value()->sendTextMessage(messageStr);
            }
        }
    }
}


void SocketServer::processTextMessage(QString message)
{
    try {
        QWebSocket *pClient = qobject_cast<QWebSocket *>(sender());
        qDebug() << "Message received:" << message;
        if (pClient) {
            QJsonDocument messageDoc = QJsonDocument::fromJson(message.toUtf8());
            QJsonObject messageObj = messageDoc.object();
            QString messageType = messageObj.value("type").toString();
            if (messageType == "subscribeToParticipantList") {
                QString meetingId = messageObj.value("meetingId").toString();
                QString userId = messageObj.value("userId").toString();
                socketClients[meetingId][userId] = pClient;
                notifyParticipantListUpdated(meetingId);
                pClient->sendTextMessage("Successfully subscribed to meeting id: "+ meetingId);
            }
            else if (messageType == "sendChatMessage"){
                QString meetingId = messageObj.value("meetingId").toString();
                QString userName = messageObj.value("userName").toString();
                QString messageText = messageObj.value("message").toString();
                addAndNotifyChatMessage(meetingId, userName, messageText);
            }
            else if (messageType == "getChatMessages"){
                QString meetingId = messageObj.value("meetingId").toString();
                QString userId = messageObj.value("userId").toString();
                socketClients[meetingId][userId] = pClient;
                if (!chatHistory.contains(meetingId)) {
                    QList<QPair<QString, QString>> history;
                    chatHistory[meetingId] = history;
                }
                QJsonArray historyArray;
                for (const auto& chat : chatHistory[meetingId]) {
                    QJsonObject chatObj;
                    chatObj.insert("sender", chat.first);
                    chatObj.insert("message", chat.second);
                    historyArray.append(chatObj);
                }
                QJsonObject chatHistoryObj;
                chatHistoryObj.insert("type", "chatMessageHistory");
                chatHistoryObj.insert("history", historyArray);
                QJsonDocument chatHistoryDoc(chatHistoryObj);
                QString chatHistoryMessageStr = QString::fromUtf8(chatHistoryDoc.toJson());
                pClient->sendTextMessage(chatHistoryMessageStr);
            }
            else{
                pClient->sendTextMessage("Unable to subscribe to meeting");
            }
        }
    } catch (...) {
        qDebug() << "Error2";
    }
}

void SocketServer::socketDisconnected()
{
    try {
        QWebSocket *pClient = qobject_cast<QWebSocket *>(sender());
        qDebug() << "socketDisconnected started:" << pClient;
        if (pClient) {
            QString meetingId = "";
            QString userId = "";
            // find the meetingId and userId for the disconnected socket
            for (auto it = socketClients.begin(); it != socketClients.end(); ++it) {
                for (auto it2 = it.value().begin(); it2 != it.value().end(); ++it2) {
                    if (it2.value() == pClient) {
                        meetingId = it.key();
                        userId = it2.key();
                        break;
                    }
                }
                if (!meetingId.isEmpty() && !userId.isEmpty()) {
                    break;
                }
            }
            if (!meetingId.isEmpty() && !userId.isEmpty()) {
                socketClients[meetingId].remove(userId);
                notifyParticipantListUpdated(meetingId);
            }
            pClient->deleteLater();
            qDebug() << "socketDisconnected";
        }
    } catch (...) {
        qDebug() << "Error3";
    }

}
