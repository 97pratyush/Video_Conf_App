#ifndef DATABASE_H
#define DATABASE_H

#include <QtCore>
#include <QJsonObject>

void setupDatabase();
int findUserDetails(QString& email, QString& password);
QString createUser(QString email, QString password, QString name);
QString createMeeting(int hostId);
QString addParticipantToMeeting(int userId, QString& participants, int meetingId);
QString removeParticipantFromMeeting(int userId, QString& participants, int meetingId);
QString joinMeeting(int userId, int meetingId);
QString endMeeting(int userId, int meetingId);

#endif // DATABASE_H
