/******
    Standard popups
******/

jQuery(function($){

    $('#other_license_blah a').prepOverlay(
	{
	    subtype:'ajax',
	    'closeselector':'[name=form.button.Cancel]',
	    formselector:'form',
	    afterpost:function () {
		//var license_name = "<span tal:replace='license_name'>license_name</span>";
		//var license_name_field = self.parent.document.getElementById('license_other_name');
		//license_name_field.setAttribute('value',license_name);
		window.close();
	    }
	}
    );

});

