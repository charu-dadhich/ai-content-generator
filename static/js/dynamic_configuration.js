var numberOfQuestions = document.getElementsByName('quantity')
var marksForQuestions = document.getElementsByName('marks')
var selectedLevel = [];
var nextBtn = document.getElementById('next-btn');
let difficultyFilledCount = 0;
var bloomLevel = document.querySelectorAll('.bloom-button')
var selectedBloomValue = document.querySelector(".selected-bloom-value")
var difficultyElement = document.querySelector('.difficulty-level')

var total = 0
var blockCount = 0
const difficultyLevel = [
    {'name': 'Easy', 'percentage': 25}, 
    {'name': 'Medium', 'percentage': 50},
    {'name': 'Difficult', 'percentage': 20},
    {'name': 'Very Challenging', 'percentage': 5}
]
const questionTypeMapping = {
    "Multiple Choice Questions": "mcqs",
    "Assertion and Reason Questions": "assertion_reason",
    "Case Based Questions": "case_based",
    "Paragraph Based Questions": "paragraph_based",
    "Fill in the blanks Questions": "fill_in_the_blanks",
    "Match the following Questions": "match_the_following",
    "Short Answer Questions": "short_answer",
    "Long Answer Questions": "long_answer",
    "Application Based Questions": "application_based",
    "Reference to Context Questions": "reference_to_context",
    "Statement Based Questions": "statement_based",
    "Parallel Questions": "parallel",
    "Writing Skill Based Questions": "writing_skill",
    "Source Based Questions": "source_based",
    "Critical Analysis Based Questions": "critical_analysis",
    "If Based Questions": "if_based"
}

function addQuestionTypeBlock() {
    const template = document.getElementById('questionTypeTemplate');
    const container = document.getElementById('questionTypeContainer');
    var newIndex = ++blockCount;
    console.log("block id count", newIndex)
    const html = template.innerHTML.replace(/_INDEX_/g, newIndex);
    console.log("html", html)
    const tempDiv = document.createElement('div');
    tempDiv.innerHTML = html;
    container.appendChild(tempDiv.firstElementChild);
    // const clone = template.content.cloneNode(true);
    // clone.id = `questionTypeTemplate-${templateTagCount++}`
    // container.appendChild(clone);
}

document.addEventListener('DOMContentLoaded', () => {
    addQuestionTypeBlock();
    window.checkQuestionsCount = function() {
        console.log("questions------",numberOfQuestions)
        let totalCount = 0
        numberOfQuestions.forEach(question => {
            console.log("question--------------------", question)
            questionValue = parseInt(question.value) || 0; 
            totalCount += questionValue;
            console.log("total", totalCount)
        });
        return totalCount;
    }
    updateQuestionCountDisplay
});

nextBtn.addEventListener('click', async function(e) {
    e.preventDefault();
    const data1String = sessionStorage.getItem('form-1-data')
    const data2String = sessionStorage.getItem('form-2-data')
    const data3String = sessionStorage.getItem('form-3-data')
    const csrftoken = getCookie('csrftoken')
    const formData = new FormData()
    // var fileContent = null;
    // var fileName = null;
    // var fileType = null;
    
    const dbRequest = indexedDB.open('PDFStorage', 1);

    dbRequest.onsuccess = function(event) {
        const db = event.target.result;
        const tx = db.transaction('pdfs', 'readwrite');
        const store = tx.objectStore('pdfs');

        const getReq = store.get('currentPdf');

        getReq.onsuccess = async function() {
            const fileData = getReq.result;

            if (!fileData) {
                console.log('No file found in IndexedDB');
                return;
            }

            const fileContent = fileData.fileContent;
            const fileName = fileData.fileName; // fix: use fileName, not fileData
            const fileType = fileData.fileType;

            function dataURLtoBlob(dataURL) {
                const parts = dataURL.split(',');
                const byteString = atob(parts[1]);
                const mimeString = parts[0].split(':')[1].split(';')[0];
                const ab = new ArrayBuffer(byteString.length);
                const ia = new Uint8Array(ab);
                for (let i = 0; i < byteString.length; i++) {
                    ia[i] = byteString.charCodeAt(i);
                }
                return new Blob([ab], { type: mimeString });
            }

            console.log('File Name:', fileName);
            const blob = dataURLtoBlob(fileContent);
            const file = new File([blob], fileName, { type: fileType });
            console.log(file);
            console.log(file instanceof File);
            console.log(file.name);
            // console.log(abc)
            const formData = new FormData(); // Make sure FormData is initialized
            formData.append('file_input', file);
            console.log('File appended to formData:', file);
            // console.log(abc)
            // Merge other data
            const data1 = data1String ? JSON.parse(data1String) : {};
            const data2 = data2String ? JSON.parse(data2String) : {};
            const data3 = data3String ? JSON.parse(data3String) : {};
            const mergedData = { ...data1, ...data2, ...data3 };

            for (const k in mergedData) {
                const value = mergedData[k];
                const isObject = typeof value === 'object' && value !== null;
                formData.append(k, isObject ? JSON.stringify(value) : value);
            }

            console.log("FormData ready to send:", [...formData.entries()]);

            // UI loading state
            document.body.classList.add('overflow-hidden', 'h-full', 'm-0');
            document.querySelector(".preload").style.display = "block";

            try {
                const response = await fetch('/questions/', {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrftoken,
                    },
                    body: formData,
                    credentials: 'same-origin'
                });

                if (!response.ok) {
                    throw new Error('Network response was not OK');
                }

                const result = await response.json();
                console.log('API response:', result);

                window.location.href = `/education-content-generator/generate-questions/${result.data.question_paper_id}/?generation_type=${data2['generation_type']}`;

            } catch (error) {
                console.error('Error posting merged data:', error);
                showToast("Got some error while generating. Please try again", true);
            } finally {
                document.body.classList.remove('overflow-hidden');
                document.querySelector(".preload").style.display = "none";
            }
        };

        getReq.onerror = function() {
            console.error('Failed to retrieve file from IndexedDB');
        };
    };
});


function getCurrentActiveBlock(selectElement, currentBlock) {
  const id = currentBlock.getAttribute('data-id');
  const type = selectElement.value;
  const marks = currentBlock.querySelector(`#marks_${id}`).value;
  const quantity = currentBlock.querySelector(`#quantity_${id}`).value;
  const existingCaseExtras = currentBlock.querySelector('.extra-case-fields');

  console.log('Current Block Values:', { type, marks, quantity });
  console.log('Selected element:', selectElement);

  if (["11", "12", "22", "18", "19"].includes(type)) {
    console.log("isnide")
    if (!existingCaseExtras) {
      const extraDiv = document.createElement('div');
      extraDiv.classList.add('extra-case-fields');
      extraDiv.innerHTML = `
        <div>
          <label for="sub_questions" class="block text-sm font-medium text-gray-700 mb-1">Total Number of Sub Questions</label>
          <input id="sub_questions" type="number" name="sub-questions" class="w-full border border-gray-300 rounded-md p-2" min="1" />
        </div>  

        <div>
          <label for="objective}" class="block text-sm font-medium text-gray-700 mb-1">Number of Objective Questions</label>
          <input type="number" id="objective" name="objective-quantity" class="w-full border border-gray-300 rounded-md p-2" min="1" />
        </div>

        <div>
          <label for="subjective" class="block text-sm font-medium text-gray-700 mb-1">Number of Subjective Questions</label>
          <input type="number" id="subjective" name="subjective-quantity" class="w-full border border-gray-300 rounded-md p-2" min="1" />
        </div>
      `;
      currentBlock.appendChild(extraDiv);
      checkTotalSubQuestions(currentBlock);
    }
  } 
  else {
    if (existingCaseExtras) {
      existingCaseExtras.remove();
    }
  }

}


function checkTotalSubQuestions(currentBlock) {
    setTimeout(() => {
    const subInput = currentBlock.querySelector('#sub_questions');
    const objInput = currentBlock.querySelector('#objective');
    const subjInput = currentBlock.querySelector('#subjective');

    const validateSubTotal = () => {
      const sub = parseInt(subInput.value) || 0;
      const obj = parseInt(objInput.value) || 0;
      const subj = parseInt(subjInput.value) || 0;

      if (sub !== obj + subj) {
        subInput.setCustomValidity('Sub-question total must equal Objective + Subjective');
        subInput.reportValidity();
      } else {
        subInput.setCustomValidity('');
      }
    };

    [objInput, subjInput].forEach(input => {
      input.addEventListener('input', validateSubTotal);
    });
  }, 0);
}



// old code
difficultyLevel.map(object => {
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
    if (diffculty_total !== 100) {
        percentageWarning.innerHTML = `
            <div class="mt-4 p-3 bg-yellow-50 border border-yellow-200 text-yellow-700 rounded-xl">
                <div class="flex items-center gap-2">
                    <span class="text-yellow-500">⚠️</span>
                    <span class="font-medium">Total percentage must equal 100%. Current total: ${diffculty_total}%</span>
                </div>
            </div>
        `
        nextBtn.disabled = true;
    }
    else {
        percentageWarning.innerHTML = '';
        nextBtn.disabled = false;
    }
};

window.checkSaveForm3Data = function() {
    var difficultyValueName = document.querySelectorAll('.difficult-level-value')
    console.log("inside form 3 saving adat functionx`")
    console.log(difficultyValueName)
    const data = {}

    difficultyValueName.forEach(difficulty => {
        const diff_value = difficulty?.value?.trim();
        console.log("diffculty", diff_value)
        console.log(difficulty.name)
        if (diff_value && diff_value !==0) {
            difficultyFilledCount ++;
            data[difficulty.name] = parseFloat(diff_value)
        }
    })
    console.log("count printinf", selectedLevel.length, difficultyFilledCount)
    if (validateAllFormBlocks() && selectedLevel.length && difficultyFilledCount > 0){
        console.log("inside form3 save")
        nextBtn.disabled = false;
        sessionStorage.removeItem('form-3-data')
        console.log("next")
        // var form3 = document.querySelector('.space-y-8')
        const blocks = document.querySelectorAll('.form-card');
        blocks.forEach((block) => {
            const id = block.getAttribute('data-id');
            const type = block.querySelector(`[name="question_type"]`);
            console.log("type of the slected block",type, type.value, typeof(type.value))
            const typeLabel = type.options[type.selectedIndex].text;
            console.log("type lable", typeLabel, questionTypeMapping[typeLabel])
            const marks = block.querySelector(`[name="marks"]`);
            const quantity = block.querySelector(`[name="quantity"]`);
            const mappedType = questionTypeMapping[typeLabel];
            let subVal = 0;
            let objVal = 0;
            let subjVal = 0;

            if (["11", "12", "22", "18", "19"].includes(type.value)) {
                console.log("in if yes")
                var sub = block.querySelector('#sub_questions');
                var obj = block.querySelector('#objective');
                var subj = block.querySelector('#subjective');
                console.log("**************sub ques",sub.value, obj.value, subj.value)
                subVal = parseInt(sub.value);
                objVal = parseInt(obj.value);
                subjVal = parseInt(subj.value);
            }
            console.log(quantity.value, marks.value, subVal, subjVal, objVal)
            data[mappedType] = JSON.stringify({
                number_of_questions: Number(quantity.value),
                marks_per_question: Number(marks.value),
                total_sub_questions: subVal,
                sub_subjective_questions: subjVal,
                sub_objective_questions: objVal,
            });            
        })
        data['bloom_filters'] = JSON.stringify(selectedLevel);
        data['total_questions'] = parseInt(total);
        data['generation_type'] = "custom";
        sessionStorage.setItem('form-3-data', JSON.stringify(data));
    }
    return ;
}

function updateQuestionCountDisplay () {
    total = checkQuestionsCount();
    console.log("total displayed ques", total)
    const display = document.querySelector('.question-count-display');
    console.log("**********",display)
    display.dataset.count = total;
    display.textContent = total;
    const warningElement = document.querySelector('.warning-element')
    console.log("warn-----", warningElement, total)
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
            if (selectedLevel.length === 0){
                nextBtn.disabled = true
            }
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
        }, 100);
    });
});

document.querySelectorAll('.bloom-button')
  .forEach(btn => {
    btn.addEventListener('click', async(e) =>{
        checkSaveForm3Data()
    })
});

document.addEventListener('input', async(e) => {
    checkSaveForm3Data()
})

function validateAllFormBlocks() {
  const blocks = document.querySelectorAll('.form-card');
  let isValid = true;

  blocks.forEach((block, index) => {
    const id = block.getAttribute('data-id');
    const type = block.querySelector(`[name="question_type"]`).value;
    const marks = block.querySelector(`[name="marks"]`);
    const quantity = block.querySelector(`[name="quantity"]`);

    // Basic field check
    if (!type || !marks.value || !quantity.value) {
      isValid = false;
      nextBtn.disabled = true;
      return;
    }

    // Check for special types needing extra fields
    if (["11", "12", "22", "18", "19"].includes(type)) {
      const sub = block.querySelector('#sub_questions');
      const obj = block.querySelector('#objective');
      const subj = block.querySelector('#subjective');

      if (!sub || !obj || !subj || !sub.value || !obj.value || !subj.value) {
        isValid = false;
        // console.warn(`Missing sub-question breakdown in block ${index + 1}`);
        nextBtn.disabled = true;
        return;
      }

      // Check if sub = obj + subj
      const subVal = parseInt(sub.value);
      const objVal = parseInt(obj.value);
      const subjVal = parseInt(subj.value);

      if (subVal !== objVal + subjVal) {
        isValid = false;
        sub.setCustomValidity('Total sub-questions must equal objective + subjective.');
        sub.reportValidity();
        nextBtn.disabled = true;
      } else {
        sub.setCustomValidity('');

      }
    }
  });
  console.log("validity check",isValid)
  return isValid;
}

var prevBtn = document.getElementById('prevBtn')
prevBtn.addEventListener('click', function() {
    history.back()
});
