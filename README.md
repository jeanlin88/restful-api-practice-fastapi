# 說明文件
## 環境建置
### Database
#### Postgres
```bash
docker volume create local-postgres-vol
docker run -d --name local-postgres \
-e POSTGRES_USER=postgres \
-e POSTGRES_PASSWORD=password \
-e PGDATA=/var/lib/postgresql/data/pgdata \
-v local-postgres-vol:/var/lib/postgresql/data \
-p 5432:5432 \
postgres
```
#### DBEaver
從windows連線到wsl中的postgres docker container
```powershell
wsl hostname -I
```
```powershell
192.168.152.27 172.17.0.1
```
dbeaver的連線方式: `192.168.152.27:5432`
## 功能
### error
```json
// status: 4xx~5xx
{
    "success": false,
    "result": null,
    "error": "error message"
}
```
### 使用者CRUD
- Create User
    > POST /api/user
    ```json
    // request body
    {
        "id": "ef04b190-6186-40c3-b5be-752f6c2bd7d4",
        "email": "test@gmail.com.tw",
        "password": "test_password",
        "name": "test_user"
    }
    ```
    ```json
    // status: 201
    {
        "success": true,
        "result": [
            {
                "id": "ef04b190-6186-40c3-b5be-752f6c2bd7d4",
                "email": "test@gmail.com.tw",
                "name": "test_user"
            }
        ]
    }
    ```
- Get All User
    > GET /api/user
    ```json
    // status: 200
    {
        "success": true,
        "result": [
            {
                "id": "ef04b190-6186-40c3-b5be-752f6c2bd7d4",
                "email": "test@gmail.com.tw",
                "name": "test_user"
            }
        ]
    }
    ```
- Get User By ID
    > GET /api/user?id=ef04b190-6186-40c3-b5be-752f6c2bd7d4
    ```json
    // status: 200
    {
        "success": true,
        "result": [
            {
                "id": "ef04b190-6186-40c3-b5be-752f6c2bd7d4",
                "email": "test@gmail.com.tw",
                "name": "test_user"
            }
        ]
    }
    ```
- Update User
    > PATCH /api/user?id=ef04b190-6186-40c3-b5be-752f6c2bd7d4
    ```json
    // request body
    {
        "password": "updated_password"
    }
    ```
    ```json
    // status: 200
    {
        "success": true,
        "result": {
            "id": "ef04b190-6186-40c3-b5be-752f6c2bd7d4",
            "email": "test@gmail.com.tw",
            "name": "test_user"
        }
    }
    ```
    ```json
    // status: 304
    ```
- Delete User
    > DELETE /api/user?id=ef04b190-6186-40c3-b5be-752f6c2bd7d4
    ```json
    // status: 204
    ```
### 登入登出
- 登入
    > POST /api/auth
    ```json
    // request body
    {
        "email": "test@gmail.com.tw",
        "password": "test_password"
    }
    ```
    ```json
    // status: 200
    {
        "success": true,
        "result": {
            "token": "jwt_token",
            "expiresAt": 1704421495
        }
    }
    ```
- 登出
    > DELETE /api/auth
    ```json
    // status: 204
    ```