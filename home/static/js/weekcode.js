function weekcode(week)
{
    w = week / 10;
    document.write("星期" + "一二三四五六日".charAt(w - 1));
    if (week % 10 == 1) document.write("下午");
    if (week % 10 == 2) document.write("晚上");
    if (week % 10 == 3) document.write("后段下午");
    if (week % 10 == 4) document.write("后段晚上");
}
