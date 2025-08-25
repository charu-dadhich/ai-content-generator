var nextBtn = document.getElementById('next-btn');
var prevBtn = document.getElementById('prevBtn')
nextBtn.disabled = false;

sessionStorage.clear()

nextBtn.addEventListener('click', async(e) => {
    e.preventDefault();
    const content = document.querySelector('.space-y-6').innerHTML
    sessionStorage.setItem('htmlContent', content)
    console.log(sessionStorage.getItem('htmlContent'))
    const previous_url = window.location.href
    const lastSlashIndex = previous_url.lastIndexOf('/')
    const lastSegment = previous_url.substring(lastSlashIndex + 2);
    // const serviceId = sessionStorage.getItem('service_type')
    window.location.href = `/education-content-generator/download-content/?service_type_id=${serviceId}&resource_id=${lastSegment}`;
});

prevBtn.addEventListener('click', function() {
    history.back()
});
