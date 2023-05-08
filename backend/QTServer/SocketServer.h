#ifndef SOCKETSERVER_H
#define SOCKETSERVER_H

#include <QtCore/QObject>
#include <QtCore/QList>
#include <QtCore/QByteArray>
#include <QtCore/QMap>
#include <QtCore/QPair>


QT_FORWARD_DECLARE_CLASS(QWebSocketServer)
QT_FORWARD_DECLARE_CLASS(QWebSocket)

class SocketServer : public QObject
{
    Q_OBJECT

public:
    explicit SocketServer(quint16 port, bool debug = false, QObject *parent = nullptr);
    ~SocketServer();

signals:
    void closed();

private slots:
    void onNewConnection();
    void processTextMessage(QString message);
    void socketDisconnected();

private:
    QWebSocketServer *webSocketServer;
    QMap<QString, QMap<QString, QWebSocket *>> socketClients;// meetingId => (userId => socket)
    QMap<QString, QList<QPair<QString, QString>>> chatHistory;// meetingId => chat history
    void notifyParticipantListUpdated(QString& meetingId);
    void addAndNotifyChatMessage(QString meetingId, QString sender, QString message);
};

#endif // SOCKETSERVER_H
