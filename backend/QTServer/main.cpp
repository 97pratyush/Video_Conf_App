#include <QtCore>
#include "socketserver.h"
#include "database.h"
#include "apihandler.h"

int main(int argc, char **argv)
{
    QCoreApplication app(argc, argv);
    setupDatabase();

    QHttpServer httpServer;
    const auto port = httpServer.listen(QHostAddress::Any, 8282);


    if (!port)
        return 0;

    httpServer.route("/", []() {
        return "Welcome to video conf application";
    });

    httpServer.route("/login", QHttpServerRequest::Method::Post, [](const QHttpServerRequest& request){
        return loginResponse(request);
    });

    httpServer.route("/createUser", QHttpServerRequest::Method::Post, [](const QHttpServerRequest& request){
        return createUserResponse(request);
    });

    httpServer.route("/createMeeting", QHttpServerRequest::Method::Post, [](const QHttpServerRequest& request){
        return createNewMeetingResponse(request);
    });

    httpServer.route("/joinMeeting", QHttpServerRequest::Method::Post, [](const QHttpServerRequest& request){
        return joinMeetingResponse(request);
    });

    httpServer.route("/endMeeting", QHttpServerRequest::Method::Post, [](const QHttpServerRequest& request){
        return endMeetingResponse(request);
    });

    qDebug() << "Running on http://127.0.0.1:"<<port;


    SocketServer *mSocket = new SocketServer(1234);
    QObject::connect(mSocket, &SocketServer::closed, &app, &QCoreApplication::quit);

    return app.exec();
}

