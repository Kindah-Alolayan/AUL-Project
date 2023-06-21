import mysql.connector as mysql
from mysql.connector import errorcode
import oss2
import os

# Table creation
# CREATE TABLE IF NOT EXISTS User (
#     id INT PRIMARY KEY,
#     name VARCHAR(50) NOT NULL,
#     email VARCHAR(50) NOT NULL,
#     password VARCHAR(50) NOT NULL,
#     password_re_enter VARCHAR(50) NOT NULL);

# CREATE TABLE IF NOT EXISTS Patient (
#     id INT PRIMARY KEY,
#     name VARCHAR(50) NOT NULL,
#     phoneNum VARCHAR(10) NOT NULL);

# CREATE TABLE IF NOT EXISTS Result (
#     patientId INT NOT NULL,
#     output VARCHAR(200) NOT NULL,
#     percentage VARCHAR(10) NOT NULL,
# 	imgPath VARCHAR(500) NOT NULL,
# 	FOREIGN KEY (patientId) REFERENCES Patient (id));


# change based on device
def insertUser(id, name, email, password, password_re_enter):
    con = mysql.connect(
        host="rm-l4vq6f07188z41kilzo.mysql.me-central-1.rds.aliyuncs.com",
        user="db_admin",
        password="1420113tM!",
        db="appdb",
    )
    cur = con.cursor()
    try:
        cur.execute(
            "INSERT INTO User (id,name,email,password,password_re_enter) VALUES (%s,%s,%s,%s,%s)",
            (int(id), str(name), str(email), str(password), str(password_re_enter)),
        )
        con.commit()
        cur.close()
        con.close()
        return True
    except mysql.Error as err:
        print(err)
        cur.close()
        con.close()
        return False


# change based on device
def retrieveUsers(id, password):
    con = mysql.connect(
        host="rm-l4vq6f07188z41kilzo.mysql.me-central-1.rds.aliyuncs.com",
        user="db_admin",
        password="1420113tM!",
        db="appdb",
    )
    cur = con.cursor()
    try:
        cur.execute(
            "SELECT id, password FROM User WHERE id = %s AND password = %s",
            (int(id), str(password)),
        )
        users = cur.fetchall()
        print(users[0][0])
        con.close()
        cur.close()
        return users
    except mysql.Error as err:
        print(err)


# save patient results
def insertResult(
    result_output,
    result_percentage,
    result_img,
    patient_name,
    patient_phone,
    patient_id,
):
    # Save to OSS
    uploadImg(result_img)
    img_OSS_path = "https://aul-bucket.oss-me-central-1.aliyuncs.com/" + result_img[99:]
    con = mysql.connect(
        host="rm-l4vq6f07188z41kilzo.mysql.me-central-1.rds.aliyuncs.com",
        user="db_admin",
        password="1420113tM!",
        db="appdb",
    )
    cur = con.cursor()
    try:
        cur.execute(
            "INSERT INTO Patient (id,name,phoneNum) VALUES (%s,%s,%s) ON DUPLICATE KEY UPDATE name=name",
            (int(patient_id), str(patient_name), str(patient_phone)),
        )
        cur.execute(
            "INSERT INTO Result (patientId,output,percentage,imgPath) VALUES (%s,%s,%s,%s)",
            (
                int(patient_id),
                str(result_output),
                str(result_percentage),
                str(img_OSS_path),
            ),
        )
        con.commit()
        cur.close()
        con.close()
        return True
    except mysql.Error as err:
        print(err)
        cur.close()
        con.close()
        return False


# upload img to OSS bucket
def uploadImg(img_path):
    # The AccessKey pair of an Alibaba Cloud account has permissions on all API operations. Using these credentials to perform operations in OSS is a high-risk operation. We recommend that you use a RAM user to call API operations or perform routine O&M. To create a RAM user, log on to the RAM console.
    auth = oss2.Auth("LTAI5tPKTft3eccdr11DLjuv", "2hIaQooAl4SK8pvk160LNS99Xefrey")
    # Specify the endpoint of the region in which the bucket is located. For example, if the bucket is located in the China (Hangzhou) region, set the endpoint to https://oss-cn-hangzhou.aliyuncs.com.
    # Specify the bucket name.
    bucket = oss2.Bucket(auth, "http://oss-me-central-1.aliyuncs.com", "aul-bucket")
    # Specify the full paths of the local file and object. The full path of the object cannot contain the bucket name.
    # By default, if you do not specify the full path of a local file, the local file is uploaded from the path of the project to which the sample program belongs.
    img = img_path[99:]
    result = bucket.put_object_from_file(img, img_path)
    # Return img url
    # Change to specific bucket


# get result info
def getResult(patient_id):
    con = mysql.connect(
        host="rm-l4vq6f07188z41kilzo.mysql.me-central-1.rds.aliyuncs.com",
        user="db_admin",
        password="1420113tM!",
        db="appdb",
    )
    print(patient_id)
    cur = con.cursor()
    try:
        # SELECT patientId, output, percentage, imgPath FROM Result WHERE patientId = %s
        cur.execute("SELECT * FROM Result WHERE patientId= %s" % patient_id)
        result = cur.fetchall()
        print("Resuls of patien:\n\n\n\n")
        print(result)
        print("\n\n\n\n")
        con.close()
        cur.close()
        return result.pop()
    except mysql.Error as err:
        print(err)


# get patient info
def getPatient(patient_id):
    con = mysql.connect(
        host="rm-l4vq6f07188z41kilzo.mysql.me-central-1.rds.aliyuncs.com",
        user="db_admin",
        password="1420113tM!",
        db="appdb",
    )
    cur = con.cursor()
    try:
        cur.execute(
            "SELECT * FROM Patient WHERE id =%s",
            (int(patient_id)),
        )
        patient = cur.fetchall()
        con.close()
        cur.close()
        return patient
    except mysql.Error as err:
        print(err)


# change based on device
def forgetPassword(name, email):
    con = mysql.connect(
        host="rm-l4vq6f07188z41kilzo.mysql.me-central-1.rds.aliyuncs.com",
        user="db_admin",
        password="1420113tM!",
        db="appdb",
    )
    cur = con.cursor()
    try:
        cur.execute(
            "SELECT  id, password  FROM User WHERE name = %s AND email = %s",
            (str(name), str(email)),
        )
        users = cur.fetchall()
        con.close()
        cur.close()
        return users
    except mysql.Error as err:
        print(err)
