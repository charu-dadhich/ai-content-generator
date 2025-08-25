// window.addEventListener('DOMContentLoaded', function () {
// //     // all your logic here
//     document.getElementById("downloadBtn").addEventListener("click", function () {
//         const elt = sessionStorage.getItem("htmlContent");
    
//         if (elt) {
//             console.log(elt)
//             // const target = document.getElementById("print-target");
//             const tempDiv = document.createElement('div');
//             tempDiv.innerHTML = elt;
//             // Inject the HTML
//             const content = tempDiv.innerText
//             console.log("xxxx",content)
//             Object.assign(tempDiv.style, {
//         position: 'absolute',
//         left: '0',
//         top: '0',
//         width: '210mm',
//         minHeight: '297mm',
//         opacity: '0',
//         pointerEvents: 'none',
//         background: 'white',
//         overflow: 'visible',
//         zIndex: '1000',
//         display: 'block',
// });
//             // Allow browser to render it before converting
//             setTimeout(() => {
//                 const opt = {
//                     margin:       0.5,
//                     filename:     'questions.pdf',
//                     image:        { type: 'jpeg', quality: 0.98 },
//                     html2canvas:  { scale: 2, useCORS: true },
//                     jsPDF:        { unit: 'in', format: 'a4', orientation: 'portrait' }
//                 };
    
//                 html2pdf().set(opt).from(tempDiv).save().then(() => {
//                     tempDiv.innerHTML = '';
//                     tempDiv.style.display = 'none';
//                 });
//             }, 2000); // Delay is key to allow rendering
//             // document.body.appendChild(target);
//         } else {
  //             alert("No content found in sessionStorage!");
  //         }
  //     });
  // });
  
window.addEventListener('DOMContentLoaded', function () {
  var prevBtn = document.getElementById('prevBtn')
  var nextBtn = this.document.getElementById('next-btn')

  nextBtn.innerText = 'Start Over'
  nextBtn.disabled = false
  nextBtn.addEventListener('click', function(){
    sessionStorage.clear()
    window.location.href = '/education-content-generator/home/'
  })

  prevBtn.addEventListener('click', function() {
    history.back()
  });

  const elt = sessionStorage.getItem('htmlContent');
  console.log(elt);
  const tempDiv = document.createElement('div');
  tempDiv.innerHTML = elt;
  tempDiv.querySelectorAll('[style*="display: none"], .collapsed, .more-text').forEach(el => el.style.display = 'inline');

  // Now get the text content
  const content = tempDiv.innerText;

  document.getElementById('downloadBtn').addEventListener('click', async () => {
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();

    const contentLines = content
      .split('\n')                     // split into lines
      .map(line => line.trim())       // trim whitespace
      .filter(line => line.length);   // remove empty lines

    // Now let jsPDF wrap lines (180 = max width)
    const wrappedLines = contentLines.flatMap(line => doc.splitTextToSize(line, 180));

    let y = 10;
    const pageHeight = doc.internal.pageSize.height;

    wrappedLines.forEach(line => {
      if (y > pageHeight - 10) {
        doc.addPage();
        y = 10;
      }
      doc.text(line, 10, y);
      y += 7;
    });

    doc.save("output.pdf");
  });
})
