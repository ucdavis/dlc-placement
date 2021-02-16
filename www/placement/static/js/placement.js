$(document).ready(function(){
	
// Load the loading icon till page is charged
	jQuery('#overlay').fadeOut();
	
// datepicker init	
	$('.datepicker').datepicker({
	    changeMonth: true,
	    changeYear: true,
	    dateFormat: "yy-mm-dd"
	});

// Clear language level options in Scoresheet page before populate with new selectios
	function clearLevelOptions(){
		$("#id_placement_level_id").html("<select class='select form-control' id='id_placement_level_id' name='placement_level_id'></select>");
	}
		
// Populate levels dropdownlist  according to selected language		
	$('#id_language_id').change(function(){
			language_id = $(this).val();
			$.ajax({
				url	: '/scoresheet/get_levels/' + language_id + '/',
				success : function(data){
					clearLevelOptions();
					$.each(data, function(key, value){
						$('#id_placement_level_id').append('<option value="' + value.pk+ '">' + value.level +'</option>');
					});
					
				}
				
			});
	});
	
	
// AJAX call to Banner for searching for STUDENT info
	$("#btn_populate").on('click',function(e){
		jQuery('#overlay').fadeIn();
		e.preventDefault();
		sid = $("#id_sid").val();
		formatted = 'json';
		clean_fields = $(this).attr('clean_fields');
		$.ajax({
			url	: "/scoresheet/GetStudentIAM/"+sid+"/"+formatted+"/",
			success	: function(data){
				if(data.length == 0){
					sid = $('#id_sid').val();
					$("#search_message").html("<li class='error'>NOT FOUND Student ID: "+sid+"</li>");
					$("#id_needs_review").val(1);
					jQuery('#overlay').fadeOut();
					if(clean_fields=='True'){
							$("#id_first_name").val("");
							$("#id_last_name").val("");
							$("#id_email").val("");
						}
							
				}else{				
				$("#search_message").html("<li class='success'>Student ID Found</li>");
				$("#id_needs_review").val(0);
						$("#id_first_name").val(data[0][0]);
						$("#id_last_name").val(data[0][1]);
						$("#id_email").val(data[0][2]);		
						jQuery('#overlay').fadeOut();
				}
				}	
								
		});
		
		
	});
	
	// AJAX call to LDAP for searching for USER info
	$("#btn_find_user").on('click',function(e){
		e.preventDefault();
		clean_fields = $(this).attr('clean_fields');
		uid = $("#id_cas_user").val();
		$.ajax({
			url	: "/users/GetUserLDAP/"+ uid +"/",

			success	: function(data){

				if( !data.first_name){
					$("#search_message").html("<li class='error'>NOT FOUND username: "+uid+"</li>");
					if(clean_fields=='True'){
						$("#id_first_name").val("");
						$("#id_last_name").val("");
						$("#id_email").val("");	
						$("#department").val("");
					}
				}else{
				$("#search_message").html("<li class='success'>User Found</li>");
						$("#id_first_name").val(data.first_name);
						$("#id_last_name").val(data.last_name);
						$("#id_department").val(data.department);
						$("#id_email").val(data.email);		
				}
				}
		});
		
	});


// check/uncheck all the languages in Languages for Users page
	$("#btn-check-all").on("click",function(e){
		e.preventDefault();		
		$("input:checkbox[name = language_id]").attr('checked',true);
		$("input:checkbox[name = language_id]").prop('checked',true);
	});
	
	$("#btn-uncheck-all").on("click",function(e){
		e.preventDefault();
	$("input:checkbox[name = language_id]").prop('checked',false);
	$("input:checkbox[name = language_id]").attr('checked',false);
});

	
});
		
			
function goBack() {
	    window.history.back();
	}

