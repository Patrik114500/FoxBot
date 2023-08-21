<!DOCTYPE html>
<html lang="hu">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <link rel="stylesheet" href="style.css"/>
    
</head>
<body>
    <div class="header">
        <div>
		<h3>FoxBot</h3>
        <img src="Main\Icon.png" alt="Foxbot icon">
        </div>
        <div>
        <p>Felhasználó:<?php
                        session_start();
                        if (isset($_SESSION['username'])) {
	                        $username = $_SESSION['username'];
	                        echo  $username;
                            
                        } 
                    ?><p>
		<button class="logout-button" onclick="logout()">Logout</button>
        </div>
        </div>
    <div class="content">                   
    <div class="container">
        <div class="chatbox">
            <div class="chatbox__support">
                <div id="canvas"><canvas id="canvas1"> </canvas></div>
                <div class="chatbox__footer">
                      <input type="text"  placeholder="Írj egy üzenetet...">
                      <button class="chatbox__send--footer send__button">Küldés</button>
                </div>
                <div class="chatbox__messages" >
                    <p id="chat" hidden="true">Szia <?php
                        if (isset($_SESSION['username'])) {
	                        $username = $_SESSION['username'];
	                        echo  $username;
                            
                        } 
                    ?>!</p>
                    
                </div>
            </div>
        </div>
    </div>

    <div class="info-panel">  
        <h1>Info</h1>           
		<div class="block">
			<div>
				<h2>Amiben tudok segíteni:</h2>
				<p>Beszélgethetsz velem és megpróbálok segítséget adni a felmerülő problémáidban. Beszélgetéseinkel lehetőséget adsz nekem, hogy mentális higéniával kapcsolatos kérdőíveket töltsek ki, ezáltal képes leszek diagnosztikákat felállítani, jelenlegi állapotodről. Ezeket a kérdőíveket külön is kitöltheted, ha a kérdőív megfelelő rövídítését megadod nekem.</p>
			</div>
			<div>
				<h2>Kérdőívek:</h2>
				<p>CDI (Gyermekdepresszió kérdőív)</p>
			</div>
			
		</div>
    </div>
    </div> 
        <footer>
                <div class="row">
                <div class="col-md-6">
                    <h4>Contact Us</h4>
                    <p>Email: <a href="mailto:info@yourwebsite.com">info@yourwebsite.com</a></p>
                </div>
                <div class="col-md-6">
                    <h4>Information</h4>
                    <ul class="list-unstyled">
                    <li><a href="#">Privacy Policy</a></li>
                    <li><a href="#">Terms of Use</a></li>
                    <li><a href="#">FAQs</a></li>
                    </ul>
                </div>
                </div>
        </footer>

    <script src="app.js"></script>
    <script src="script.js"></script>

    <?php
    echo '<script>var sessionId = "' . $username . '";</script>';
    ?>
    
    <script>
		function logout() {
			window.location.href = 'logout.php';
        }
	</script>
    
</body>
</html>