// import { getCookie } from "./base";
var nextBtn = document.getElementById('next-btn');
var selectedLevel = [];
let difficultyFilledCount = 0;
var bloomLevel = document.querySelectorAll('.bloom-button')
var selectedBloomValue = document.querySelector(".selected-bloom-value")
var difficultyElement = document.querySelector('.difficulty-level')
let numberOfQuestions = document.querySelectorAll('.question-type-value')
var difficultyValueName = document.querySelectorAll('.level-name')
var total = 0


console.log("level elt dom", difficultyElement)

const difficultyLevel = [
    {'name': 'Easy', 'percentage': 25}, 
    {'name': 'Medium', 'percentage': 50},
    {'name': 'Difficult', 'percentage': 20},
    {'name': 'Very Challenging', 'percentage': 5}
]

const questionTypeMapping = [
    {1: 'subjective_2_marks'},
    {2: 'subjective_4_marks'},
    {3: 'objective_2_options'},
    {4: 'objective_4_options'},
    {5: 'case_based'},
    {6: 'fill_ups'},
    {7: 'match_ups'},
]
document.addEventListener('DOMContentLoaded', function () {
    window.handleQuestionTypeChange = function(type, count) {
        updateQuestionCountDisplay();
    }

    window.handleWordCountChange = function(type, count) {
        let b = parseInt(count) || 0;
    }

    window.checkQuestionsCount = function() {
        console.log("questions------",numberOfQuestions)
        let totalCount = 0
        numberOfQuestions.forEach(question => {
            questionValue = parseInt(question.value) || 0; 
            totalCount += questionValue;
            console.log("total", totalCount)
        });
        return totalCount;
    }

    function updateQuestionCountDisplay () {
        total = checkQuestionsCount();
        const display = document.querySelector('.question-count-display');
        console.log("**********",display)
        display.dataset.count = total;
        display.textContent = total;
        const warningElement = document.querySelector('.warning-element')
        if (total > 15) {
            console.log("here")
            warningElement.classList.add(
                'mt-6', 'p-4', 'bg-red-50', 'border', 'border-red-200', 'text-red-700', 'rounded-xl'
            )
            warningElement.innerHTML = `<div class="flex items-center gap-2">
                <span class="text-red-500">⚠️</span>
                <span class="font-medium">Total questions ${total} exceeds the maximum limit of 15. Please adjust.</span>
            </div>`
        }
        else {
            warningElement.innerHTML = '';
            warningElement.classList.remove('mt-6', 'p-4', 'bg-red-50', 'border', 'border-red-200', 'text-red-700', 'rounded-xl')
        }
    }
    console.log("bloom level",bloomLevel)

    
    console.log("elt diff", difficultyElement)

    difficultyLevel.map(object => {
        // console.log("inside diffcult level", object)
        difficultyElement.innerHTML += `
            <div class="text-center">
                <label class="level-name block text-sm font-medium text-gray-700 mb-2">
                    ${object.name}
                </label>
                <div class="relative">
                    <input name= ${object.name.toLowerCase().replace(/\s+/g, '_')}_percentage type="number" min="0" max="100" value=${object.percentage} onchange="checkDifficultyPercentage()"
                            class="difficult-level-value w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500 text-center">
                    <span class="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 text-sm">%</span>
                </div>
            </div>
        `
        // console.log("great",difficultyElement.innerHTML)
        difficultyFilledCount ++;
    });

    
    function getDifficultyTotal () {
        var difficultyLevelValue = document.querySelectorAll('.difficult-level-value') 
        console.log("inside diffculty lebel", difficultyLevelValue)
        var totalDifficulty = 0;
        console.log("chcking")
        difficultyLevelValue.forEach(elt => {
            console.log("di",elt)
            var difficultyValue = parseFloat(elt.value) || 0
            totalDifficulty += difficultyValue
        })
        return totalDifficulty;
    }

    window.checkDifficultyPercentage = function () {
        var diffculty_total = getDifficultyTotal()
        var percentageWarning = document.querySelector('.percentage-warning')
        // console.log(total, typeof(total))
        if (diffculty_total !== 100) {
            percentageWarning.innerHTML = `
                <div class="mt-4 p-3 bg-yellow-50 border border-yellow-200 text-yellow-700 rounded-xl">
                    <div class="flex items-center gap-2">
                        <span class="text-yellow-500">⚠️</span>
                        <span class="font-medium">Total percentage must equal 100%. Current total: ${diffculty_total}%</span>
                    </div>
                </div>
            `
        }
        else {
            percentageWarning.innerHTML = '';
        }
    };

    // checkDifficultyPercentage();

    window.checkSaveForm3Data = function() {
        console.log("inside form 3 saving adat functionx`")
        
        let filledCount = 0;
        
        
        numberOfQuestions.forEach(question => { 
            console.log("abc--",question.value, typeof(question.value))
            const ques_value = question?.value?.trim(); // optional chaining
            // console.log("ques", question, question.id.split('-')[0])
            if (ques_value && ques_value !==0) {
                console.log("in if", ques_value.id)
                filledCount ++;
                var key = parseInt(question.id.split('-')[0])
                mapping = questionTypeMapping.find(item => item[key])
                question.name = mapping[key]
                console.log("name", question.name)
            }
        })
        
        difficultyValueName.forEach(difficulty => {
            const diff_value = difficulty?.value?.trim();
            console.log("diffculty", diff_value)
            console.log(difficulty.name)
            if (diff_value && diff_value !==0) {
                difficultyFilledCount ++;
                // var key = parseInt(difficulty.id.split('-')[0])
                // mapping = questionTypeMapping.find(item => item[key])
                // difficulty.name = mapping[key]
            }
        })
        // if (filledCount === 0) {
        //     alert("Please fill in at least one field.");
        //     return;
        // }
        // if (selectedLevel.length === 0) {
        //     alert("Please select at least one of the options from the blooms taxonomy.")
        // }
        console.log("selected---",selectedLevel, selectedLevel.length)
        console.log("---------->",numberOfQuestions, difficultyValueName, filledCount)
        console.log(filledCount, difficultyFilledCount, selectedLevel.length)
        console.log(filledCount > 0 && selectedLevel.length && difficultyFilledCount > 0)
        if (filledCount > 0 && selectedLevel.length && difficultyFilledCount > 0) {
            console.log("inside form3 save")
            nextBtn.disabled = false;
            sessionStorage.removeItem('form-3-data')
            console.log("next")
            var form3 = document.querySelector('.space-y-8')
            // const form3Data = new FormData()
            const data = {};
            form3.querySelectorAll('input[name]').forEach(el => {
                var form3Key = el.name
                var form3Value = parseInt(el.value) || 0
                data[form3Key] = form3Value
            });
            // console.log("bloom_filters", selectedLevel)
            // sessionStorage.setItem('form-3-data', JSON.stringify('bloom_filters', selectedLevel))
            // sessionStorage.setItem('form-3-data', JSON.stringify('total_questions', parseInt(total)))
            // sessionStorage.setItem('form-3-data', JSON.stringify("generation_type", "custom")
            data['bloom_filters'] = JSON.stringify(selectedLevel);
            data['total_questions'] = parseInt(total);
            data['generation_type'] = "custom";
            sessionStorage.setItem('form-3-data', JSON.stringify(data));
            // sessionStorage.setItem('form-3-data', data)
            console.log("done", sessionStorage.getItem('form-3-data'))
        }
    }
});

document.addEventListener('input', async(e) => {
    checkSaveForm3Data()
})

document.querySelectorAll('.bloom-button')
  .forEach(btn => {
    btn.addEventListener('click', async(e) =>{
        checkSaveForm3Data()
    })
});

nextBtn.addEventListener('click', async(e) => {
    checkSaveForm3Data();
    e.preventDefault();
    const data1String = sessionStorage.getItem('form-1-data')
    const data2String = sessionStorage.getItem('form-2-data')
    const data3String = sessionStorage.getItem('form-3-data')
    const csrftoken = getCookie('csrftoken')

    const formData = new FormData()

    const fileContent = localStorage.getItem('fileContent');
    const fileName = localStorage.getItem('fileName');
    const fileType = localStorage.getItem('fileType');
    // formData.append('total_questions', parseInt(total))
    // console.log("bloom_filters", selectedLevel)
    // formData.append('bloom_filters', selectedLevel)

    function dataURLtoBlob(dataURL) {
        const parts = dataURL.split(',');
        const byteString = atob(parts[1]); // Decode base64 string
        const mimeString = parts[0].split(':')[1].split(';')[0]; // Get MIME type

        const ab = new ArrayBuffer(byteString.length);
        const ia = new Uint8Array(ab);

        for (let i = 0; i < byteString.length; i++) {
            ia[i] = byteString.charCodeAt(i);
        }

        return new Blob([ab], { type: mimeString });
    }

    if (fileContent) {
        // Example: Display an image if it's a Data URL
        // const img = document.createElement('img');
        // img.src = fileContent;
        // document.body.appendChild(img);
        console.log('File Name:', fileName);
        const blob = dataURLtoBlob(fileContent)
        const file = new File([blob], fileName, { type: fileType });
        formData.append('file_input', file)
        console.log(fileContent)
        // form
    } else {
        console.log('No file content found.');
    }


    // console.log(data1String)
    // console.log(data2String)
    // console.log(data3String)
    const data1 = data1String ? JSON.parse(data1String) : {};
    const data2 = data2String ? JSON.parse(data2String) : {};
    const data3 = data3String ? JSON.parse(data3String) : {};
    mergedData = {...data1, ...data2, ...data3}
    console.log(mergedData)
    for (const k in mergedData) {
        formData.append(k, mergedData[k]);
    }
    // const file = window.sharedUploadFile;
    console.log("her esi teh file from 2 page",fileContent)
    // if (file) {
    //     formData.append("file_input", file);
    // }
    console.log("data of form upto 1 to 3", formData)
    try {
        const response = await fetch('/questions/', {
        method: 'POST',
        headers: {
        //     // 'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken, 
        },
        body: formData,
        credentials: 'same-origin'
        });
        
        if (!response.ok) {
        throw new Error('Network response was not OK');
        }

        const result = await response.json();
        console.log(result.data)
        console.log('API response:', result, result.data);
        window.location.href =  `/education-content-generator/generate-questions/${result.data.question_paper_id}`;

    } catch (error) {
        console.error('Error posting merged data:', error);
        // setTimeout(() => {
        //     console.clear();
        // }, 18000);
    }
})

bloomLevel.forEach(function(el) {
    var selectedIdArray = new Array(5).fill(false);
    const color = {
        'bloom-level-1': ['bg-red-100', 'text-red-800', 'border-red-300', 'border-current', 'shadow-md', 'selected'],
        'bloom-level-2': ['bg-orange-100', 'text-orange-800', 'border-orange-300', 'border-current', 'shadow-md', 'selected'],
        'bloom-level-3': ['bg-yellow-100', 'text-yellow-800', 'border-yellow-300', 'border-current', 'shadow-md', 'selected'],
        'bloom-level-4': ['bg-green-100', 'text-green-800', 'border-green-300', 'border-current', 'shadow-md', 'selected'],
        'bloom-level-5': ['bg-blue-100', 'text-blue-800', 'border-blue-300', 'border-current', 'shadow-md', 'selected'],
        'bloom-level-6': ['bg-purple-100', 'text-purple-800', 'border-purple-300', 'border-current', 'shadow-md', 'selected']
    }
    el.addEventListener('click', function() {
        bloomIndividualLevel = document.getElementById(`${this.id}`)
        var levelId = bloomIndividualLevel.dataset.id
        console.log('level', levelId)
        selectedIdArray[levelId-1] = !selectedIdArray[levelId-1]
        console.log(bloomIndividualLevel.id)
        if (selectedIdArray[levelId-1]) {
            console.log("in if")
            bloomIndividualLevel.classList.add(...color[bloomIndividualLevel.id])
            bloomIndividualLevel.classList.remove('border-gray-200', 'hover:shadow-md', 'hover:border-gray-300', 'bg-white')
            console.log(bloomIndividualLevel.classList)
            selectedLevel.push(Number(levelId))
            console.log("sle", selectedLevel)
        }
        else{
            bloomIndividualLevel.classList.remove(...color[bloomIndividualLevel.id])
            selectedLevel.pop(levelId)
        }
        
        setTimeout(() => {
            console.log("here",selectedLevel)
            selectedBloomValue.innerText = 'Selected: ';
            selectedLevel.forEach(level => {
                console.log("isnide", level)
                var selectBloomElement = document.querySelector(`#bloom-level-${level}`)
                const text = selectBloomElement.querySelector('.font-medium.text-sm').innerText;
                console.log("elt", selectBloomElement, text)
                selectedBloomValue.innerText += " "+ text + ",  "
                console.log(selectedBloomValue)
            })
        }, 200);
    });
});

var prevBtn = document.getElementById('prevBtn')
prevBtn.addEventListener('click', function() {
    history.back()
});
