// Invitation Code Generator for Django Admin
(function($) {
    $(document).ready(function() {
        // Wait for DOM to be ready
        setTimeout(function() {
            var codeField = $('#id_code');
            
            if (codeField.length && !codeField.prop('readonly')) {
                // Create generate button
                var generateBtn = $('<button type="button" class="button" style="margin-left: 10px; vertical-align: middle;">' +
                    '<i class="fas fa-random"></i> Zufälliger Code generieren' +
                    '</button>');
                
                // Add button after code field
                codeField.after(generateBtn);
                
                // Add help text
                var helpText = $('<p class="help" style="color: #666; font-size: 12px; margin-top: 5px;">' +
                    'Format: Nur Großbuchstaben (A-Z) und Zahlen (0-9). Bindestriche (-) sind erlaubt.<br>' +
                    'Beispiel: IFTAR2024-ABC123 oder einfach ABC123XYZ' +
                    '</p>');
                generateBtn.after(helpText);
                
                // Generate random code function
                function generateRandomCode() {
                    // Karışık karakterleri hariç tut: 0 (sıfır), O (harf), I (harf), 1 (rakam)
                    // Sadece net karakterler: A-H, J-N, P-Z (I ve O yok) ve 2-9 (0 ve 1 yok)
                    var chars = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
                    var code = '';
                    for (var i = 0; i < 6; i++) {
                        code += chars.charAt(Math.floor(Math.random() * chars.length));
                    }
                    return code;
                }
                
                // Button click handler
                generateBtn.click(function() {
                    var randomCode = generateRandomCode();
                    codeField.val(randomCode);
                    codeField.focus();
                    
                    // Visual feedback
                    codeField.css('background-color', '#d4edda');
                    setTimeout(function() {
                        codeField.css('background-color', '');
                    }, 1000);
                });
                
                // Auto-convert to uppercase on input
                codeField.on('input', function() {
                    var cursorPos = this.selectionStart;
                    var value = $(this).val();
                    var newValue = value.toUpperCase();
                    
                    // Only allow A-Z, 0-9, and hyphen
                    newValue = newValue.replace(/[^A-Z0-9-]/g, '');
                    
                    if (value !== newValue) {
                        $(this).val(newValue);
                        // Restore cursor position
                        this.setSelectionRange(cursorPos, cursorPos);
                    }
                });
                
                // Validation on blur
                codeField.on('blur', function() {
                    var value = $(this).val().trim();
                    if (value && !/^[A-Z0-9-]+$/.test(value)) {
                        alert('Einladungscode darf nur Großbuchstaben (A-Z), Zahlen (0-9) und Bindestriche (-) enthalten.');
                        $(this).focus();
                    }
                });
            }
        }, 500);
    });
})(django.jQuery);
