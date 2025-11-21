var nextBtn = document.getElementById('next-btn');
nextBtn.disabled = false;
let serviceId = null;

nextBtn.addEventListener('click', async(e) => {
    e.preventDefault();
    const content = document.querySelector('.space-y-8').innerHTML
    sessionStorage.setItem('htmlContent', content)
    console.log(sessionStorage.getItem('htmlContent'))
    const previous_url = new URL(window.location.href)
    // const lastSlashIndex = previous_url.lastIndexOf('/')
    // const lastSegment = previous_url.substring(lastSlashIndex + 1)
    const pathSegments = previous_url.pathname.split('/').filter(Boolean)
    const id = pathSegments[pathSegments.length - 1]
    const formDataStr = sessionStorage.getItem('form-2-data');

    if (formDataStr) {
        const formData = JSON.parse(formDataStr);
        serviceId = formData['service_type_id'];
    } else {
        console.warn('form-2-data not found in sessionStorage');
    }
    window.location.href = `/education-content-generator/download-content/?service_type_id=${serviceId}&resource_id=${id}`;
});