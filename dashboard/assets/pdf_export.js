// PDF Export for Dash Report
// This script triggers html2pdf.js to export the report section as a PDF when the button is clicked.

window.addEventListener('DOMContentLoaded', function() {
    var btn = document.getElementById('download-pdf-btn');
    if (!btn) return;
    btn.addEventListener('click', function() {
        var reportDiv = document.querySelector('.report-main-content');
        if (!reportDiv) {
            alert('Report content not found!');
            return;
        }
        if (typeof window.html2pdf === 'undefined') {
            alert('PDF export library not loaded!');
            return;
        }
        html2pdf().from(reportDiv).save('Business_Report.pdf');
    });
}); 
