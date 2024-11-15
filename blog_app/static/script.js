// دالة لفتح الشريط الجانبي
function openSidebar() {
    document.getElementById("sidebar").style.width = "250px";  // عرض الشريط الجانبي
    document.getElementById("mainContent").classList.add("opened");  // تعديل محتوى الصفحة
}

// دالة لإغلاق الشريط الجانبي
function closeSidebar() {
    document.getElementById("sidebar").style.width = "0";  // إخفاء الشريط الجانبي
    document.getElementById("mainContent").classList.remove("opened");  // استعادة الوضع الطبيعي للمحتوى
}


document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");

    form.addEventListener("submit", function (event) {
        // مثال للتحقق من إدخال جميع الحقول قبل الإرسال
        const title = form.querySelector("#id_title").value.trim();
        const author = form.querySelector("#id_author").value.trim();

        if (title === "" || author === "") {
            event.preventDefault();
            alert("يرجى ملء جميع الحقول المطلوبة.");
        }
    });
});





function toggleMenu(icon) {  // تغيير الحروف الصغيرة إلى الكبيرة
    const dropdown = icon.nextElementSibling;
    if (dropdown.style.display === "none" || dropdown.style.display === "") {
        dropdown.style.display = "block";
    } else {
        dropdown.style.display = "none";
    }
}

document.addEventListener('click', function(event) {
    const menu = document.querySelectorAll('.options-menu');
    menu.forEach(function(item) {
        const dropdown = item.querySelector('.dropdown-content');
        // إذا تم الضغط خارج القائمة أو الأيقونة، سيتم إخفاء القائمة
        if (!item.contains(event.target) && dropdown.style.display === "block") {
            dropdown.style.display = 'none'; // إخفاء القائمة إذا تم الضغط خارجها
        }
    });
});



