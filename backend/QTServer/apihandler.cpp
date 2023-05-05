#include "apihandler.h"

QHttpServerResponse loginResponse(const QHttpServerRequest& request){
    try {
        QJsonObject loginInfo = QJsonDocument::fromJson(request.body()).object();
        QString email = loginInfo.value("email").toString();
        QString password = loginInfo.value("password").toString();
        QStringList userDetails = findUserDetails(email, password);
        if(!userDetails.isEmpty()){
            QJsonObject response = {{"message", "Login Success"}, {"id", userDetails[0]}, {"email", email}, {"name", userDetails[1]}};
            return QHttpServerResponse(response, QHttpServerResponse::StatusCode::Ok);
        }
        else{
            QJsonObject response = {{"message", "Invalid Credentials!!"}};
            return QHttpServerResponse(response, QHttpServerResponse::StatusCode::Unauthorized);
        }
    } catch (QException e) {
        return QHttpServerResponse(e.what(),QHttpServerResponder::StatusCode::InternalServerError);
    }
}

QHttpServerResponse createUserResponse(const QHttpServerRequest& request){
    try {
        QJsonObject userInfo = QJsonDocument::fromJson(request.body()).object();
        QString email = userInfo.value("email").toString();
        QString password = userInfo.value("password").toString();
        QString name = userInfo.value("name").toString();
        QString userId = createUser(email, password, name);
        if(userId != "error"){
            QJsonObject response = {{"message", "User Creation Success"}, {"userId", userId}, {"email", email}, {"name", name}};
            return QHttpServerResponse(response, QHttpServerResponse::StatusCode::Ok);
        }
        else{
            QJsonObject response = {{"message", "User Already Exists"}};
            return QHttpServerResponse(response, QHttpServerResponse::StatusCode::Forbidden);
        }

    } catch (QException e) {
        return QHttpServerResponse(e.what(),QHttpServerResponder::StatusCode::InternalServerError);
    }
}

QHttpServerResponse createNewMeetingResponse(const QHttpServerRequest& request){
    try {
        QJsonObject meetingInfo = QJsonDocument::fromJson(request.body()).object();
        int hostId = meetingInfo.value("userId").toInt();
        QString meetingId = createMeeting(hostId);
        if(meetingId != "error"){
            QJsonObject response = {{"message", "Meeting created"}, {"meetingId", meetingId}, {"hostId", hostId}};
            return QHttpServerResponse(response, QHttpServerResponse::StatusCode::Ok);
        }
        else{
            QJsonObject response = {{"message", "Unable to create meeting"}};
            return QHttpServerResponse(response, QHttpServerResponse::StatusCode::InternalServerError);
        }

    } catch (QException e) {
        return QHttpServerResponse(e.what(),QHttpServerResponder::StatusCode::InternalServerError);
    }
}

QHttpServerResponse joinMeetingResponse(const QHttpServerRequest& request){
    try {
        QJsonObject meetingInfo = QJsonDocument::fromJson(request.body()).object();
        int userId = meetingInfo.value("userId").toInt();
        int meetingId = meetingInfo.value("meetingId").toInt();
        qDebug() << "meetingInfo: "<<userId << meetingId;
        QString participantsInfo = joinMeeting(userId, meetingId);
        if(participantsInfo != "error"){
            QJsonObject response = {{"message", "Meeting Joined"}, {"meetingId", meetingId}, {"participants", participantsInfo}};
            return QHttpServerResponse(response, QHttpServerResponse::StatusCode::Ok);
        }
        else{
            QJsonObject response = {{"message", "Unable to join meeting"}};
            return QHttpServerResponse(response, QHttpServerResponse::StatusCode::InternalServerError);
        }

    } catch (QException e) {
        return QHttpServerResponse(e.what(),QHttpServerResponder::StatusCode::InternalServerError);
    }
}

QHttpServerResponse endMeetingResponse(const QHttpServerRequest& request){
    try {
        QJsonObject meetingInfo = QJsonDocument::fromJson(request.body()).object();
        int userId = meetingInfo.value("userId").toInt();
        int meetingId = meetingInfo.value("meetingId").toInt();
        qDebug() << "meetingInfo: "<<userId << meetingId;
        QString participantsInfo = endMeeting(userId, meetingId);
        if(participantsInfo != "error"){
            QJsonObject response = {{"message", "Removed participant from meeting"}, {"meetingId", meetingId}, {"participants", participantsInfo}};
            return QHttpServerResponse(response, QHttpServerResponse::StatusCode::Ok);
        }
        else{
            QJsonObject response = {{"message", "Unable to join meeting"}};
            return QHttpServerResponse(response, QHttpServerResponse::StatusCode::InternalServerError);
        }

    } catch (QException e) {
        return QHttpServerResponse(e.what(),QHttpServerResponder::StatusCode::InternalServerError);
    }
}
