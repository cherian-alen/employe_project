$(document).ready(function(){
    $("#sub").click(function(){
        if ($("#id_name").val()==""){
            alert("Enter Name")
            return false;
        }
        if($("#id_email").val()==""){
            alert("Enter Email")
            return false;
         }
         if(!$("#id_email").val().match('^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')){
            alert("Enter Email")
            return false;
         }
         if($("#id_contact").val()==""){
            alert("Enter Contact")
            return false;
         }
         if ($("#id_contact").val().length < 10) {
            alert("Contact number should be at least 10 digits");
            return false;
         }
         if($("#id_password").val()==""){
            alert("Enter Password")
            return false;
         }
    })
})