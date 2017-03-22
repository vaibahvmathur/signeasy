/**
 * Created by Vaibhav on 22-03-2017.
 */
$(document).ready(function(){
    $(".delete_btn").on("click",function(){
        var id = $(this).attr('id');
        $('#confirm_delete').modal('show');
        $('#delete_user').on('click', function(){
            $.ajax({
                type : 'POST',
                url : "deleteuser/",
                data : { 'id' : id },
                dataType : 'json'
            }).done(function(json){
                var result = json.message;
                if(result == "success"){
                    $('#confirm_delete').modal('hide');
                    alert('Success')
                    location.href = '#'
                    location.reload();
                }
                else if( result == "error" ){
                    $('#confirm_delete').modal('hide');
                    alert('error while deleting');
                }
                else{
                    $('#confirm_delete').modal('hide');
                    alert('error while deleting')
                }
            }).fail(function(){
                $('#confirm_delete').modal('hide');
                alert("failed while deleting")
            });
        });
    });
});