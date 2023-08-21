<?php

require_once "config.php";
 

$username = $password = $confirm_password = "";
$username_err = $password_err = $confirm_password_err = "";
$lastuid = 1;

if($_SERVER["REQUEST_METHOD"] == "POST"){
 function test_input($data) {
	
	$data = trim($data);
	$data = stripslashes($data);
	$data = htmlspecialchars($data);
	return $data;
}

    if(empty(trim($_POST["username"]))){
        $username_err = "Kérem, adjon meg felhasználónevet.";
    } elseif(!preg_match('/^[a-zA-Z0-9_]+$/', trim($_POST["username"]))){
        $username_err = "A felhasználónév csak betűket, számokat és underscore-okat tartalmazhat.";
    } else{
      
        $stmt = $conn->prepare("SELECT * FROM user");
	    $stmt->execute();
	    $users = $stmt->fetchAll();

        foreach($users as $user) {
            if($user['username'] == $username) 
                 {
                echo "<script language='javascript'>";
                echo "alert('WRONG INFORMATION')";
                echo "</script>";
                die();
            }
            else {
                $lastuid++;
                $username = strval(test_input($_POST["username"]));
            }
        }
    }
    
  
    if(empty(trim($_POST["password"]))){
        $password_err = "Kérem, adjon meg egy jelszót.";     
    } elseif(strlen(trim($_POST["password"])) < 6){
        $password_err = "A jelszónak legalább 6 karaktert tartalmaznia kell.";
    } else{
        $password = strval(test_input($_POST["password"]));
    }
    
    
    if(empty(trim($_POST["confirm_password"]))){
        $confirm_password_err = "Kérem erősítse meg a jelszavát.";     
    } else{
        $confirm_password = trim($_POST["confirm_password"]);
        if(empty($password_err) && ($password != $confirm_password)){
            $confirm_password_err = "Nem eggyező jelszó.";
        }
    }
    
  
    if(empty($username_err) && empty($password_err) && empty($confirm_password_err)){
        
       
        $stmt = $conn->prepare("INSERT INTO cdi (id) VALUES ($lastuid)");
	    $stmt->execute();
        $stmt = $conn->prepare("INSERT INTO user (username,password,CDIid) VALUES ('$username','$password',$lastuid)");
	    $stmt->execute();
        header("location: login.php");
    }
    
}
?>
 
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Sign Up</title>
    <link rel="stylesheet" href="log.css">
    <style>
        body{ font: 14px sans-serif; }
        .wrapper{ width: 360px; padding: 20px; }
    </style>
</head>
<body>
<img class="logo" src="Main\FoxRegister.png" alt="">
    <div class="login-box">
        <form  action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]); ?>" method="post">
            <div class="textbox">
                <input type="text" name="username" placeholder="Felhasználónév" class="form-control  <?php echo (!empty($username_err)) ? 'is-invalid' : ''; ?>" value="<?php echo $username; ?>">
                <span class="invalid-feedback"><?php echo $username_err; ?></span>
            </div>    
            <div class="textbox">
                <input type="password" name="password" placeholder="Jelszó" class="form-control <?php echo (!empty($password_err)) ? 'is-invalid' : ''; ?>" value="<?php echo $password; ?>">
                <span class="invalid-feedback"><?php echo $password_err; ?></span>
            </div>
            <div class="textbox">
                <input type="password" name="confirm_password" placeholder="Jelszó megerősítése" class="form-control <?php echo (!empty($confirm_password_err)) ? 'is-invalid' : ''; ?>" value="<?php echo $confirm_password; ?>">
                <span class="invalid-feedback"><?php echo $confirm_password_err; ?></span>
            </div>
            
                <input type="submit" class="button" value="Regisztrálás">
                <input type="reset" class="button" value="Újratölt">
            <p>Már regisztráltál? Bejelentkezés <a href="login.php">itt</a>.</p>
        </form>
    </div>    
</body>
</html>