// import { getCookie } from "./base";
var nextBtn = document.getElementById('next-btn');
var prevBtn = document.getElementById('prevBtn')
const fileInput = document.getElementById('file-upload');
var questionType = document.querySelector('.question-type');
var language = document.querySelector('.language-type');
var topic = document.getElementById('topic');
var subTopic = document.getElementById('sub-topic');
var objective = document.getElementById('objective');
let selectedFile = null;
var learningObjective = document.querySelector('.learning-objective-area')
var learningObjectiveInput = document.getElementById('learning-objective')
var apiUrl = null
var serviceTypeValue = 0
var formFields = document.querySelector('.the-hidden-one'); 

window.onload = function() {
    const serviceElement = document.querySelector('.question-type')
    console.log("inside loading fucntion for fetching service type")
    console.log("local storage", sessionStorage.getItem('fileName'))
    if (serviceElement.options.length <= 1) {
        console.log("in")
        fetchQuestionType(serviceElement)
    }
    // const havedata = JSON.parse(sessionStorage.getItem('form-2-data'));
    // if(havedata){
    //     Object.entries(havedata).forEach(([key, value]) => {
    //         console.log(`Key: ${key}, Value: ${value}`);
            
    //         // Example: if you want to populate fields with values
    //         const input = document.querySelector(`[name="${key}"]`);
    //         console.log("input is", input)
    //         if (input) {
    //             input.value = value;
    //         }
    //     });
    // }
    
}

function fetchQuestionType(serviceElement) {
    console.log("her in fetching question type")
    fetch(`/education-content-generator/utils/question-type`)
    .then(response => response.json())
    .then(data => {
        console.log(data)
        const question_types = data.data || []
        question_types.forEach(type => {
            const option = document.createElement('option')
            option.value = type.id
            option.textContent = type.service_type
            console.log(option)
            serviceElement.appendChild(option)
        });      
    })
    .catch(error => {
        console.error("Error fetching board data:", error);
    });
}

document.addEventListener('DOMContentLoaded', function () {
    const fileNameDisplay = document.getElementById('file-name-display');
    const fileNameWrapper = document.getElementById('uploaded-file-name');
    let generationSelectedValue = null;
    const autoOption = document.getElementById('option-1');
    const customOption = document.getElementById('option-2');
    nextBtn.disabled = true;
    let isClicked = false;
    let customIsClicked = false;
    // const fileName = document.getElementById('#file-name-display')
    // if (sessionStorage.getItem('fileName')){
    //     console.log("inside yes local storage")
    //     fileNameDisplay.innerText = "✓ " + sessionStorage.getItem('fileName')
    //     console.log(fileNameDisplay.value, fileInput, sessionStorage.getItem('fileName'))
    //     fileNameDisplay.classList.remove('hidden')
    //     selectedFile = sessionStorage.getItem('fileContent')
    // }
    const form2data = JSON.parse(sessionStorage.getItem('form-2-data'))
    if (form2data){
        nextBtn.disabled = false
        if (form2data['generation_type'] === "option-1"){
            isClicked = true;
        }
        else{
            customIsClicked = true
            topic.value = form2data['sub_topic']
        }
        if (form2data['service_type_id']) {
            questionType.value = form2data['service_type_id']
        }
        if(form2data['topic'])[
            topic.value = form2data['topic']
        ]
        if(form2data['sub_topic'])[
        ]

    }
    autoOption.addEventListener('mouseenter', function () {
    if (isClicked) {
        // Clicked + hovered: blue border/bg, no scale
        autoOption.classList.remove('scale-105');
        autoOption.classList.add('border-blue-500', 'bg-blue-50', 'shadow-lg');
        autoOption.classList.remove('border-gray-200', 'hover:border-blue-300', 'hover:shadow-md', 'bg-white');
    } else {
        // Hover only (not clicked): blue border/bg, no scale
        autoOption.classList.add('border-blue-500', 'bg-blue-50', 'shadow-lg');
        autoOption.classList.remove('border-gray-200', 'hover:border-blue-300', 'hover:shadow-md', 'bg-white');
    }
    });

    autoOption.addEventListener('click', function () {
    isClicked = !isClicked; // toggle click state

    if (isClicked) {
        // If clicked, add border/bg but scale only if mouse is NOT hovering
        if (!autoOption.matches(':hover')) {
        autoOption.classList.add('scale-105');
        }
        autoOption.classList.add('border-blue-500', 'bg-blue-50', 'shadow-lg');
        autoOption.classList.remove('border-gray-200', 'hover:border-blue-300', 'hover:shadow-md', 'bg-white');
    } else {
        // If unclicked, revert all styles to default
        autoOption.classList.remove('scale-105', 'border-blue-500', 'bg-blue-50', 'shadow-lg');
        autoOption.classList.add('border-gray-200', 'hover:border-blue-300', 'hover:shadow-md', 'bg-white');
    }
    });

    autoOption.addEventListener('mouseleave', function () {
    if (isClicked) {
        // If clicked and mouse leaves, scale up
        autoOption.classList.add('scale-105');
        autoOption.classList.add('border-blue-500', 'bg-blue-50', 'shadow-lg');
        autoOption.classList.remove('border-gray-200', 'hover:border-blue-300', 'hover:shadow-md', 'bg-white');
    } else {
        // Not clicked: revert to default
        autoOption.classList.remove('scale-105', 'border-blue-500', 'bg-blue-50', 'shadow-lg');
        autoOption.classList.add('border-gray-200', 'hover:border-blue-300', 'hover:shadow-md', 'bg-white');
  }
});


    customOption.addEventListener('mouseenter', function () {
    if (customIsClicked) {
        // Clicked + hovered: blue border/bg, no scale
        customOption.classList.remove('scale-105');
        customOption.classList.add('border-purple-500', 'bg-purple-50', 'shadow-lg');
        customOption.classList.remove('border-gray-200', 'hover:border-purple-300', 'hover:shadow-md', 'bg-white');
    } else {
        // Hover only (not clicked): blue border/bg, no scale
        customOption.classList.add('border-purple-500', 'bg-purple-50', 'shadow-lg');
        customOption.classList.remove('border-gray-200', 'hover:border-purple-300', 'hover:shadow-md', 'bg-white');
    }
    });

    customOption.addEventListener('click', function () {
    customIsClicked = !customIsClicked; // toggle click state

    if (customIsClicked) {
        // If clicked, add border/bg but scale only if mouse is NOT hovering
        if (!customOption.matches(':hover')) {
        customOption.classList.add('scale-105');
        }
        customOption.classList.add('border-purple-500', 'bg-purple-50', 'shadow-lg');
        customOption.classList.remove('border-gray-200', 'hover:border-blue-300', 'hover:shadow-md', 'bg-white');
    } else {
        // If unclicked, revert all styles to default
        customOption.classList.remove('scale-105', 'border-purple-500', 'bg-purple-50', 'shadow-lg');
        customOption.classList.add('border-gray-200', 'hover:border-purple-300', 'hover:shadow-md', 'bg-white');
    }
    });

    customOption.addEventListener('mouseleave', function () {
        if (customIsClicked) {
            // If clicked and mouse leaves, scale up
            customOption.classList.add('scale-105');
            customOption.classList.add('border-purple-500', 'bg-purple-50', 'shadow-lg');
            customOption.classList.remove('border-gray-200', 'hover:border-purple-300', 'hover:shadow-md', 'bg-white');
        } else {
            // Not clicked: revert to default
            customOption.classList.remove('scale-105', 'border-purple-500', 'bg-purple-50', 'shadow-lg');
            customOption.classList.add('border-gray-200', 'hover:border-purple-300', 'hover:shadow-md', 'bg-white');
        }
    });

    
    fileInput.addEventListener('change', function () {
        selectedFile = this.files[0];
        console.log("selected file in file input event listener", selectedFile)
        if (selectedFile) {
            fileNameDisplay.textContent = `✓ ${selectedFile.name}`;
        }
    });
});

document.querySelectorAll(".generation-selection").forEach(function(el) {
    el.addEventListener('click', function() {
        
        generationSelectedValue = this.id;
        var inputFileTile = document.querySelector('.file-document');
        console.log(inputFileTile)
        if (generationSelectedValue){
            console.log("selected value", generationSelectedValue)
            var fileDocument = document.querySelector('.space-y-6')
            fileDocument.classList.remove('hidden')
            fileDocument.classList.add('block')
        }
        if (generationSelectedValue === "option-1") {
            formFields.classList.remove('hidden');
            // nextBtn.disabled = true
        } else if (generationSelectedValue === "option-2") {
            console.log("jere")
            formFields.classList.add('hidden');
            inputFileTile.classList.remove('hidden');
            inputFileTile.classList.add('block');
            // nextBtn.disabled = true
            checkSaveFields();
        } 
    });
});

function checkSaveFields(){
    console.log("checking elts", generationSelectedValue, learningObjectiveInput.value)
    if (generationSelectedValue === "option-1") {
        console.log("valu inside if ", language.value, questionType.value, fileInput.files.length)
        let hasError = false;
        if (questionType.value == 19){
            console.log(Number(learningObjectiveInput.value))
            if (Number(learningObjectiveInput.value) < 1 || Number(learningObjectiveInput.value) > 10) {
                hasError = true;
            }
            if (hasError){nextBtn.disabled = true; document.getElementById('error-number_of_lo').textContent = 'Must be less than or equal to 10';return;}
            else {document.getElementById('error-number_of_lo').textContent = ''}
        }
        // else{

        // }
    }
    else {
        sessionStorage.removeItem('form-2-data')
        learningObjective.classList.add('hidden')
        console.log("lese", fileInput?.files.length)
        // if (questionType.value && language.value && fileInput?.files.length > 0 ) {
        //     console.log("in if", fileInput.files[0], fileInput.files)
        //     nextBtn.disabled = false
        // }
        // else{
            nextBtn.disabled = true
        // }
    }
    if (questionType.value && language.value && fileInput?.files.length > 0) {
        console.log("qustion type((((((((((", questionType, language, fileInput, learningObjective)
        nextBtn.disabled = false;
        sessionStorage.removeItem('form-2-data')
        sessionStorage.setItem('form-2-data', JSON.stringify({
            language: language.value,
            service_type_id: Number(questionType.value),
            objective: objective?.value,
            topic: topic?.value,
            sub_topic: subTopic?.value,
            generation_type: generationSelectedValue === "option-1"? "custom": "auto",
            file_input: selectedFile,
            number_of_lo: learningObjectiveInput.value?Number(learningObjectiveInput.value):10
        }));
    }
}

function serviceTypeChange(e){
    serviceTypeValue = Number(e.target.value)
    checkSaveFields()
    if (serviceTypeValue === 19 ){
        formFields.classList.add('hidden')
        if (generationSelectedValue === "option-1"){
            learningObjective.classList.remove('hidden')
            learningObjective.classList.add('block')
        }
        console.log("here in if 19", e.target, learningObjective)
        apiUrl = '/learning-objectives/'
    }
    else{
        console.log("in else part", generationSelectedValue)
        if (generationSelectedValue === "option-1"){
            console.log("inside")
            formFields.classList.add('block');
            formFields.classList.remove('hidden')
        }
        learningObjective.classList.add('hidden')
        apiUrl = '/questions/'
    }
}

questionType.addEventListener('change', serviceTypeChange);
language.addEventListener('change', checkSaveFields);
fileInput.addEventListener('change', checkSaveFields);
topic.addEventListener('input', checkSaveFields);
subTopic.addEventListener('input', checkSaveFields);
learningObjective.addEventListener('input', checkSaveFields);

prevBtn.addEventListener('click', function() {
    history.back()
});

nextBtn.addEventListener('click', async(e) => {
    e.preventDefault();
    console.log("inside event next", generationSelectedValue)
    const data1String = sessionStorage.getItem('form-1-data');
    const data2String = sessionStorage.getItem('form-2-data');
    const data1 = data1String ? JSON.parse(data1String) : {};
    const data2 = data2String ? JSON.parse(data2String) : {};
    const mergedData = { ...data1, ...data2 };
    const csrftoken = getCookie('csrftoken');
    console.log(mergedData)
    const formData = new FormData();
    for (const key in mergedData) {
        formData.append(key, mergedData[key]);
    }
    console.log("hre is selcted file", selectedFile)
    if (selectedFile) {
        const dbRequest = indexedDB.open('PDFStorage', 1);

        dbRequest.onupgradeneeded = function(event) {
            const db = event.target.result;
            if (!db.objectStoreNames.contains('pdfs')) {
            db.createObjectStore('pdfs', { keyPath: 'id' });
            }
        };

        dbRequest.onsuccess = function(event) {
            const db = event.target.result;

            const reader = new FileReader();
            reader.onload = function(e) {
            const tx = db.transaction('pdfs', 'readwrite');
            const store = tx.objectStore('pdfs');

            store.put({
                id: 'currentPdf',
                fileContent: e.target.result,
                fileName: selectedFile.name,
                fileType: selectedFile.type
            });

            tx.oncomplete = function() {
                console.log('Data saved successfully');

                // Now read back the data
                const readTx = db.transaction('pdfs', 'readonly');
                const readStore = readTx.objectStore('pdfs');
                const getReq = readStore.get('currentPdf');

                getReq.onsuccess = function() {
                const fileData = getReq.result;
                console.log('Read from DB:', fileData);
                };

                getReq.onerror = function() {
                console.error('Failed to read data');
                };
            };

            tx.onerror = function(e) {
                console.error('Transaction failed', e.target.error);
            };
            };

            reader.readAsDataURL(selectedFile);
        };

        dbRequest.onerror = function(event) {
            console.error('DB open error', event.target.error);
        };
        // const countTx = db.transaction('pdfs', 'readonly');
        // const store = countTx.objectStore('pdfs');
        // const countReq = store.count();

        // countReq.onsuccess = function() {
        // console.log('Total entries in pdfs:', countReq.result);
        // };

    }


        // console.log("inside file if")
        // const reader = new FileReader();
        // console.log(reader)
        // reader.onload = function(e) {
        //     window.pdfFile = JSON.stringify({
        //         fileContent: e.target.result,
        //         fileName: selectedFile.name,
        //         fileType: selectedFile.type
        //     });
            // const fileDataUrl = e.target.result; 
            // console.log("url", fileDataUrl)
            // sessionStorage.setItem('fileContent', fileDataUrl);
            // sessionStorage.setItem('fileName', selectedFile.name);
            // sessionStorage.setItem('fileType', selectedFile.type);
            // console.log("here")
        // console.log("selected file------", selectedFile)
        // reader.readAsDataURL(selectedFile);
        // console.log(reader.readAsDataURL(selectedFile))
    console.log(formData, serviceTypeValue, typeof(serviceTypeValue))
    if (serviceTypeValue !== 19) {
        // document.querySelector(".preload").style.display = "block";
        // init()
        console.log("api end")
        console.log(apiUrl)
        formData.append("file_input", selectedFile)
        // formData.append("generation_type", "auto")
        sessionStorage.removeItem('form-3-data')
        if (generationSelectedValue === 'option-1') {
            console.log("inside option2 at 316")
            window.location.href = '/education-content-generator/fill-custom-data/'
            return;
        }
        document.body.classList.add('overflow-hidden');
        document.body.classList.add('h-full', 'm-0')
        document.querySelector(".preload").style.display = "block";
        init()
        try {
            const response = await fetch(apiUrl, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken
                },
                body: formData
            });
            
            if (!response.ok) {
                console.log("inside show toast ")
                // throw new Error('Network response was not OK');
                showToast("Got some error while generating. Please try again", true)
                document.body.classList.remove('overflow-hidden');
                document.querySelector(".preload").style.display = "none";
                return;
            }
            document.body.classList.remove('overflow-hidden');
            document.querySelector(".preload").style.display = "none";
            const result = await response.json();
            console.log(result.data)
            console.log('API response:', result, result.data.question_paper_id);
            window.location.href =  `/education-content-generator/generate-questions/${result.data.question_paper_id}`;
            
        } catch (error) {
            console.error('Error posting merged data:', error);
            showToast("Got some error while generating. Please try again", true)
            document.body.classList.remove('overflow-hidden');
            document.querySelector(".preload").style.display = "none";
            return;
        }
    }
    else if (serviceTypeValue === 19) {
        document.body.classList.add('overflow-hidden');
        document.querySelector(".preload").style.display = "block";
        init()
        console.log("inside else", serviceTypeValue)
        console.log("api end")
        console.log(apiUrl)
        formData.append("file_input", selectedFile)
        formData.append("generation_type", "auto")
        sessionStorage.removeItem('form-3-data')
        try {
            const response = await fetch(apiUrl, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken
                },
                body: formData
            });
            
            const result = await response.json();
            
            if (!response.ok || result.status === false) {
                console.error("Backend error:", result);
                document.body.classList.remove('overflow-hidden');
                document.querySelector(".preload").style.display = "none";
                document.body.classList.add('h-full', 'm-0')
                showToast("Got some error while generating. Please try again", true)
                return;
            }
            document.body.classList.remove('overflow-hidden');
            document.querySelector(".preload").style.display = "none";
            window.location.href =  `/education-content-generator/learning-objectives/${result.data.id}`;
        } catch (error) {
            console.error('Error posting merged data:', error);
            document.body.classList.remove('overflow-hidden');
            document.querySelector(".preload").style.display = "none";
            document.body.classList.add('h-full', 'm-0')
            showToast("Got some error while generating. Please try again", true)
        }
    }
    // else {
        
    // }      
});
