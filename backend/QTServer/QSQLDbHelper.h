#ifndef QSQLDBHELPER_H
#define QSQLDBHELPER_H

#include <QtSql>
#include <QString>
#include <QDebug>

class QSQLDbHelper
{
public:
    QSQLDbHelper(const char* driver);
    ~QSQLDbHelper();
    QSqlDatabase* connect( const QString& server,
                           const QString& databaseName,
                           const QString& userName,
                           const QString& password );
    void disConnect();

    int selectRowCountResult(QSqlQuery* query);
    QStringList selectQuery(QSqlQuery* query, int count);
    bool executeInsert(QSqlQuery* query);
    bool executeUpdate(QSqlQuery* query);
    bool executeDelete(QSqlQuery* query);

private:
    QSqlDatabase* db;
};

#endif // QSQLDBHELPER_H
