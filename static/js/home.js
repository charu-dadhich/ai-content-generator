let nextBtn = null;
let prevBtn = null;


window.onload = async function() {

    // const navEntries = performance.getEntriesByType('navigation');
    // if (navEntries.length > 0 && navEntries[0].type === 'reload') {
    //     sessionStorage.clear();
    //     console.log('Session storage cleared on reload');
    // }
    console.log("here")
    const selectElement = document.querySelector('.school-board');
    const gradeSelect = document.querySelector('.school-grade');
    console.log(selectElement)
    const havedata = JSON.parse(sessionStorage.getItem('form-1-data'));
    if (havedata) {
        console.log("inside have data")
        const subjectSelect = document.querySelector('.subject-name');
        await fetchBoardData(selectElement)
        gradeSelect.disabled=false
        await fetchGradeData(gradeSelect, havedata)
        console.log("this is only done when upper garde function is completed", subjectSelect.value = havedata.subject_id)
        subjectSelect.value = havedata.subject_id;
        return;
    }
    if (selectElement.options.length <= 1) {
        console.log("inside")
        fetchBoardData(selectElement);
    }

    selectElement.addEventListener('change', function() {
        const selectedText = this.options[this.selectedIndex].text;              
        const selectedValue = this.value;
        console.log("val",selectedValue)
        if (selectedValue) {
            const gradeSelect = document.querySelector('.school-grade');
            gradeSelect.disabled = false;
            console.log("checking data")
            fetchGradeData(gradeSelect);
            if (gradeSelect.options.length <= 1) {
                console.log("fetch grade")
            }
        }
    });
};


async function fetchBoardData(selectElement) {
  selectElement.innerHTML = '<option value="">Choose Board</option>'; 
  try {
    const response = await fetch(`/education-content-generator/utils/board/all/`);
    const data = await response.json();
    const boards = data.data || [];

    boards.forEach(board => {
      const option = document.createElement('option');
      option.value = board.id;
      option.textContent = board.name;
      selectElement.appendChild(option);
    });

    const page1 = sessionStorage.getItem('form-1-data');
    const data1 = JSON.parse(page1);
    console.log("nw data", data1, data1?.board_id);

    if (data1?.board_id) {
      selectElement.value = data1.board_id.toString();
      console.log(selectElement);
    }
  } catch (error) {
    console.error("Error fetching board data:", error);
  }
}

async function fetchGradeData(gradeSelect, haveData) {
    gradeSelect.innerHTML = '<option value="">Choose Grade</option>';
    console.log("heree")
    fetch(`/education-content-generator/utils/grade/all/`)
    .then(response => response.json())
    .then(async data => {
        const grades = data.data || [];
        grades.forEach(grade => {
            const option = document.createElement('option');
            option.value = grade.id;
            option.textContent = grade.name;
            gradeSelect.appendChild(option);
        });
        gradeSelect.classList.remove('disabled');
        const page1 = sessionStorage.getItem('form-1-data');
        const data1 = JSON.parse(page1);
        if (data1?.standard_id) {
          gradeSelect.value = data1.standard_id;
          console.log(gradeSelect, gradeSelect.value)
        }
        console.log("inside if block to call subject")
        await fetchSelectedOption(gradeSelect, fetchSubjectData, 'subject-name', haveData);
    })
    .catch(error => {
        console.error("Error fetching board data:", error);
    });
    console.log("calling the fetch select optoion")
    
}

async function fetchSelectedOption(element, function_to_call, className, haveData=false){
    console.log(" iam here", element)
    const nextElement = document.querySelector(`.${className}`);
    var selectedValue = element.value;
    console.log("selected value-----", selectedValue)
    if (haveData){
        await function_to_call(nextElement, selectedValue, haveData);
    }
    else{
    element.addEventListener('change', function() {
        console.log("chnage event inside")
        const selectedText = this.options[this.selectedIndex].text;              
        console.log("val",this.value)
        if (this.value) {
            selectedValue = this.value
            console.log(className)
            console.log('next', nextElement)
            nextElement.disabled = false;
            console.log("checking data")
            function_to_call(nextElement, selectedValue, haveData);
            if (nextElement.options.length <= 1) {
                console.log("fetch grade")
            }
        }
    });}
}

async function fetchSubjectData(subjectSelect, gradeId, haveData){
    subjectSelect.innerHTML = '<option value="">Choose Subject</option>';
    console.log("heree in ", gradeId)
    var grades = [];
    fetch(`/education-content-generator/utils/grade/${gradeId}/subjects/`)
    .then(response => response.json())
    .then(async data => {
        grades = data.data
        console.log(grades)
        grades.forEach(grade => {
            const option = document.createElement('option');
            option.value = grade.id;
            option.textContent = grade.name;
            subjectSelect.appendChild(option);
        });
        subjectSelect.disabled=false
        if (haveData){
            subjectSelect.value = haveData.subject_id
        }
        await fetchSelectedOption(subjectSelect, fetchChapterData, 'chapter-name', haveData)
    })
    .catch(error => {
        console.error("Error fetching board data:", error);
    });
}

function fetchChapterData(chapterSelect, subjectId, haveData){
    console.log("chapter", subjectId)
    let lastFetchedSubjectId = null;
    if (subjectId === lastFetchedSubjectId) {
        return;
    }
    var grades = []
    lastFetchedSubjectId = subjectId;
    chapterSelect.innerHTML = '<option value="">Choose Chapter</option>';
    console.log(lastFetchedSubjectId, subjectId)
    console.log("heree")
    fetch(`/education-content-generator/utils/subject/${subjectId}/chapters/`)
    .then(response => response.json())
    .then(async data => {
        grades = data.data;
        console.log(grades)
        grades.forEach(grade => {
            const option = document.createElement('option');
            option.value = grade.id;
            option.textContent = grade.title;
            chapterSelect.appendChild(option);
        });
        chapterSelect.disabled=false
        if (haveData){
            console.log("inside if", chapterSelect.subject_id)
            chapterSelect.value = haveData.chapter_id
        }
    })
    .catch(error => {
        console.error("Error fetching board data:", error);
    });
}

document.addEventListener('DOMContentLoaded', function () {
    const board = document.querySelector('.school-board');
    const grade = document.querySelector('.school-grade');
    const subject = document.querySelector('.subject-name');
    const chapter = document.querySelector('.chapter-name');
    nextBtn = document.getElementById('next-btn');
    prevBtn = document.getElementById('prevBtn')
    // Start with Next disabled
    nextBtn.disabled = false;
    prevBtn.disabled = true;

    function allFieldsFilled() {
        console.log("this is the place where",board.value && grade.value && subject.value && chapter.value)
        return board.value && grade.value && subject.value && chapter.value;
    }

    function maybeEnableNext() {
        if (allFieldsFilled()) {
            nextBtn.disabled = false;

            sessionStorage.setItem('form-1-data', JSON.stringify({
                board_id: Number(board.value),
                standard_id: Number(grade.value),
                subject_id: Number(subject.value),
                chapter_id: Number(chapter.value)
            }));
        } else {
            nextBtn.disabled = true;
        }
    }
    if (sessionStorage.getItem('form-1-data')){
        nextBtn.disabled=false
    }
    chapter.addEventListener('change', maybeEnableNext);
    nextBtn.addEventListener('click', (e) => {
        e.preventDefault();
        window.location.href = '/education-content-generator/fill-content-configuration/'
    });
});
