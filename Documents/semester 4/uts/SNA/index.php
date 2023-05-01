<?php
    $con = mysqli_connect('mysql_db', 'root', 'pass', 'Redlock');
    
    $data = [];
    $result = $con->query("SELECT * FROM users");
    while($row = $result->fetch_assoc()) array_push($data, $row);
?>

<!DOCTYPE html>
<body>
    <table>
        <tr>
            <th>ID</th>
            <th>Nama</th>
            <th>Alamat</th>
            <th>Jabatan</th>
        </tr>
        <?php foreach($data as $d){?>
            <tr>
                <td><?=$d["ID"]?></td>
                <td><?=$d["Nama"]?></td>
                <td><?=$d["Alamat"]?></td>
                <td><?=$d["Jabatan"]?></td>
            </tr>
        <?php } ?>
    </table>
</body>
</html>