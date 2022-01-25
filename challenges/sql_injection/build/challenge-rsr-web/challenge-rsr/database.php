<?php 
  function OpenConnection()  
  {  
      try  
      {  
          $dsn = 'mysql:host=localhost;dbname=challenge';
          $user = 'root';
          $password = 'Password123?';
          $options = array(
            PDO::MYSQL_ATTR_INIT_COMMAND => 'SET NAMES utf8',
          );
          $conn = new PDO($dsn, $user, $password,$options);
          $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
          $conn->exec("SET CHARACTER SET utf8");

          return $conn;
              
      }  
      catch(Exception $e)  
      {  
          echo($e->getMessage());  
      }  
      
  }  

?>
