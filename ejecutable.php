<?php
    $command = escapeshellcmd('finalCode.ipynb');
    $output = shell_exec($command);
    echo $output;
?>