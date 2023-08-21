<!DOCTYPE html>
<html lang="hu">
 
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <link rel="stylesheet" href="log.css">
    <title>Login Page</title>
</head>
 
<body>
    <img class="logo" src="Main\FoxLogin.png" alt="">
    <form action="validate.php" method="post">
        <div class="login-box">
           
 
            <div class="textbox">
                <i class="fa fa-user" aria-hidden="true"></i>
                <input type="text" placeholder="Felhasználónév"
                         name="username" value="">
            </div>
 
            <div class="textbox">
                <i class="fa fa-lock" aria-hidden="true"></i>
                <input type="password" placeholder="Jelszó"
                         name="password" value="">
            </div>
 
            <input class="button" type="submit"
                     name="login" value="Belépés">
            <p>Ha nincs még felhasználód, regisztrálj <a href='register.php'>itt</a></p>
        </div>

    </form>
        

</body>
 
</html>