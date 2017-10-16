$('#get-address').unbind('click');
$('#get-address').click(function (e) {
    e.preventDefault();
    create_contract($('#chal-id').val(), $('#nonce').val())
});

$('#submit-address').unbind('click');
$('#submit-address').click(function (e) {
    e.preventDefault();
    test_address($('#address-input').val(), $('#nonce').val())
});

$("#address-input").keyup(function(event){
    if(event.keyCode == 13){
        $("#submit-key").click();
    }
});

$('#submit-key').unbind('click');
$('#submit-key').click(function (e) {
    e.preventDefault();
    submitkey($('#chal-id').val(), $('#answer-input').val(), $('#nonce').val())
});

$("#answer-input").keyup(function(event){
    if(event.keyCode == 13){
        $("#submit-key").click();
    }
});

$(".input-field").bind({
    focus: function() {
        $(this).parent().addClass('input--filled' );
        $label = $(this).siblings(".input-label");
    },
    blur: function() {
        if ($(this).val() === '') {
            $(this).parent().removeClass('input--filled' );
            $label = $(this).siblings(".input-label");
            $label.removeClass('input--hide' );
        }
    }
});
var content = $('.chal-desc').text();
var decoded = $('<textarea/>').html(content).val()

$('.chal-desc').html(marked(content, {'gfm':true, 'breaks':true}));

function test_address(address, nonce) { // sends a post request to the right place to test if it was correctly solved
    $.post(script_root + "/ethereum/test", {
        address: address,
        nonce: nonce
    }, function (data) {
        $("#check-result-message").text(data);
        $("#check-address-result-notification").css("display", "inherit");
    })
}

function create_contract(chal, nonce) { // Sends a post request to the necessary place to create the challenge, and displays the address
    $("#address-loading-symbol").css("display", "inherit");
    $.post(script_root + "/ethereum/create", {
        chal: chal,
        nonce: nonce
    }, function (data) {
        $("#address-message").text(data);
        $("#address-notification").css("display", "inherit");
        $("#address-loading-symbol").css("display", "none");
    });
}
