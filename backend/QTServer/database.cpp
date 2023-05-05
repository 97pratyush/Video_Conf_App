#include "database.h"
#include "QSQLDbHelper.h"

QSQLDbHelper* qSQLDbHelper;
QSqlDatabase* db;

void setupDatabase(){
    const char* driverName = "QPSQL";
    qSQLDbHelper = new QSQLDbHelper(driverName);
    db = qSQLDbHelper->connect("localhost", "video-conf-db", "postgres", "admin");
    if(db->open()){
        qDebug() << "Db connected";
    }
    else {
        qDebug() << "Something went Wrong:" << db->lastError().text();
    }
}

QStringList findUserDetails(QString& email, QString& password){
    QSqlQuery* query = new QSqlQuery(*db);
    QStringList queryResult;
    query->setForwardOnly(true);
    if( !query->prepare(QString("SELECT id, name from public.user where email = ? and password = ?")) )
    {
        qDebug() <<"Error = " << db->lastError().text();
        return queryResult;
    }
    else{
        query->addBindValue(email);
        query->addBindValue(password);
    }
    queryResult = qSQLDbHelper->selectQuery(query, 2);
    if(queryResult.isEmpty()){
        qDebug() << "Invalid Creds";
        return queryResult;
    }
    qDebug() << "Result" << queryResult[0] << "\n";
    return queryResult;
}

QString createUser(QString email, QString password, QString name){
    QSqlQuery* query = new QSqlQuery(*db);
    query->setForwardOnly(true);
    if( !query->prepare(QString("INSERT INTO public.user( name, email, password) VALUES ( ?, ?, ?)")) )
    {
        qDebug() <<"Error = " << db->lastError().text();
        return "error";
    }
    else{
        query->addBindValue(name);
        query->addBindValue(email);
        query->addBindValue(password);
    }
    bool result = qSQLDbHelper->executeInsert(query);
    if( result ){
        qDebug() << "Successful insert";
        QString userId = query->lastInsertId().toString();
        qDebug() << "Last ID was:" << userId;
        return userId;
    }
    else{
        qDebug() << "Insert failed - User already exists";
        return "error";
    }

}

QString createMeeting(int hostId){
    QSqlQuery* query = new QSqlQuery(*db);
    query->setForwardOnly(true);
    if( !query->prepare(QString("INSERT INTO public.meeting(host, participants) VALUES (?,?)")) )
    {
        qDebug() <<"Error = " << db->lastError().text();
        return "error";
    }
    else{
        query->addBindValue(hostId);
        query->addBindValue(QString("%1,").arg(hostId));
    }
    bool result = qSQLDbHelper->executeInsert(query);
    if( result ){
        qDebug() << "Successful insert";
        QString meetingId = query->lastInsertId().toString();
        qDebug() << "Last ID was:" << meetingId;
        return meetingId;
    }
    else{
        qDebug() << "Insert failed - User already exists";
        return "error";
    }

}

QString addParticipantToMeeting(int userId, QString& participants, int meetingId){
    try {
        QStringList currentUsers = participants.split(',');
        if(currentUsers.contains(QString("%1").arg(userId))){ //user already in participants
            return participants;
        }
        QString updatedUsers = participants.append(QString("%1,").arg(userId));
        QSqlQuery* query = new QSqlQuery(*db);
        query->setForwardOnly(true);
        if( !query->prepare(QString("UPDATE public.meeting SET participants = ? WHERE id = ?")) )
        {
            qDebug() <<"Error = " << db->lastError().text();
            return "error";
        }
        else{
            query->addBindValue(updatedUsers);
            query->addBindValue(meetingId);
        }
        bool result = qSQLDbHelper->executeUpdate(query);
        if(result){
            return updatedUsers;
        }
        return "error";
    } catch (...) {
        return "error";
    }
}

QString removeParticipantFromMeeting(int userId, QString& participants, int meetingId){
    try {
        QStringList currentUsers = participants.split(',');
        if(currentUsers.contains(QString("%1").arg(userId)) == false){ //user not in participants
            return participants;
        }
        currentUsers.removeAll(QString("%1").arg(userId));
        QString updatedUsers = currentUsers.join(',');
        QSqlQuery* query = new QSqlQuery(*db);
        query->setForwardOnly(true);
        if( !query->prepare(QString("UPDATE public.meeting SET participants = ?, isactive = ? WHERE id = ?")) )
        {
            qDebug() <<"Error = " << db->lastError().text();
            return "error";
        }
        else{
            query->addBindValue(updatedUsers);
            query->addBindValue(!updatedUsers.isEmpty());
            query->addBindValue(meetingId);
        }
        bool result = qSQLDbHelper->executeUpdate(query);
        if(result){
            return updatedUsers;
        }
        return "error";
    } catch (...) {
        return "error";
    }
}

QString joinMeeting(int userId, int meetingId){
    QSqlQuery* query = new QSqlQuery(*db);
    query->setForwardOnly(true);
    if( !query->prepare(QString("SELECT host, participants from public.meeting where isactive = true and id = ?")) )
    {
        qDebug() <<"Error:joinMeeting-" << db->lastError().text();
        return "error";
    }
    else{
        query->addBindValue(meetingId);
    }
    QStringList queryResult = qSQLDbHelper->selectQuery(query, 2);
    if(queryResult.isEmpty()){
        qDebug() << "No active meeting with given id found";
        return "error";
    }
    QString participants = queryResult[1];
    QString updatedParticipant = addParticipantToMeeting(userId, participants, meetingId);
    if(updatedParticipant != "error") return updatedParticipant;
    return "error";
}

QString endMeeting(int userId, int meetingId){
    QSqlQuery* query = new QSqlQuery(*db);
    query->setForwardOnly(true);
    if( !query->prepare(QString("SELECT host, participants from public.meeting where isactive = true and id = ?")) )
    {
        qDebug() <<"Error:endMeeting-" << db->lastError().text();
        return "error";
    }
    else{
        query->addBindValue(meetingId);
    }
    QStringList queryResult = qSQLDbHelper->selectQuery(query, 2);
    if(queryResult.isEmpty()){
        qDebug() << "No active meeting with given id found";
        return "error";
    }
    QString participants = queryResult[1];
    QString updatedParticipant = removeParticipantFromMeeting(userId, participants, meetingId);
    if(updatedParticipant != "error") return updatedParticipant;
    return "error";
}
