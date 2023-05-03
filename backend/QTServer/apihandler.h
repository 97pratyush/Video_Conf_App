#ifndef APIHANDLER_H
#define APIHANDLER_H

#include <QJsonObject>
#include <QtHttpServer>
#include "database.h"

QHttpServerResponse loginResponse(const QHttpServerRequest& request);
QHttpServerResponse createUserResponse(const QHttpServerRequest& request);
QHttpServerResponse createNewMeetingResponse(const QHttpServerRequest& request);
QHttpServerResponse joinMeetingResponse(const QHttpServerRequest& request);
QHttpServerResponse endMeetingResponse(const QHttpServerRequest& request);

#endif // APIHANDLER_H
