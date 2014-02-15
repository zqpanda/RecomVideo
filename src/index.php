<html>
<head>
    <title>RecomVideo</title>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <link type="text/css" rel="stylesheet" href="../duplicate.css"/>
</head>
<body>
<?php
/***************************************************************************
 * 
 * Copyright (c) 2014 Baidu.com, Inc. All Rights Reserved
 * 
 **************************************************************************/
 
 
 
/**
 * @file index.php
 * @author zhouqiang(zhouqiang@baidu.com)
 * @date 2014/02/11 11:29:24
 * @brief 
 * 视频推荐展示工具
 *  
 **/

$dbc = mysqli_connect('10.48.47.34','xiaoling','xiaoling','video_recom_ar',6001) or die('Error connecting to MySQL server.');
//获取影片资源信息
#$set_query = "set names utf8";
#$temp = mysqli_query($dbc,$set_query);
$query = "select * from movie_raw_data";
$result = mysqli_query($dbc,$query) or die('Error querying database.no.1');

$movie_info = array();
while ($row = mysqli_fetch_array($result)){
    if (array_key_exists($row['title'],$movie_info)){
        continue;
    } else {
        $movie_info[$row['title']] = $row;
    }
}
//var_dump($movie_info);exit;
//视频TopList
$sql = "select title,score,update_time from movie_score order by score desc limit 0,100";
$query_list = mysqli_query($dbc,$sql) or die('Error querying database.no.2');
$top_list = array();
$index = 0;
while ($record = mysqli_fetch_array($query_list)){
    $top_list[$index] = array(
        'title' => $record['title'],
        'score' => $record['score'],
        'update_time' => $record['update_time'],    
    );
    $index += 1;
}
//var_dump($top_list);exit;

//url资源信息
$url_query = "select * from url_info";
$url_result = mysqli_query($dbc,$url_query) or die('Error querying database.no.3');
$url_info = array();
while ($line = mysqli_fetch_array($url_result)){
    $url_info[$line['url_name']] = $line['url_resource'];
}
//var_dump($url_info);exit;
//影片信息展示
echo '<div id="title">'.埃及视频影视推荐.'</div>';
echo '<p></p>';
echo '<div id="content"><table width="1000"><tr><th>Rank</th><th>Title</th><th>Score</th><th>Poster</th><th>Update_Time</th></tr>';
foreach($top_list as $num => $item){
    $title = $item['title'];
    $score = $item['score'];
    $update_time = $item['update_time'];
    $raw_site = $movie_info[$title]['source_site'];
    $flag = strpos($raw_site,'_');
    $site_name = $flag?substr($raw_site,0,$flag):$raw_site; 
    $pic_url = $movie_info[$title]['pic_url']; 
    if (!preg_match('/^http.*/',$pic_url)){
        $pic_url = $url_info[$site_name].$movie_info[$title]['pic_url'];
    }
    echo '<tr>';
    echo '<td>'.strval($num+1).'</td>';
    echo '<td>'.$title.'</td>';
    echo '<td>'.$score.'</td>';
    echo '<td><img src=\''.$pic_url.'\' width="100" height="120"/></td>';
    echo '<td>'.$update_time.'</td>';
    echo '</tr>'; 
}
echo '</table></div>';
/* vim: set expandtab ts=4 sw=4 sts=4 tw=100: */
?>
</body>
</html>
