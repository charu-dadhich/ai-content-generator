const loader = document.querySelector('.preload');
// loader.classList.add('hidden')


function getCookie(name) {
  let cookieValue = null;
  console.log("1", cookieValue, document.cookie)
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    console.log(cookies ,"---------->2")
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      console.log("cookie", cookie)
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        console.log(cookieValue)
        break;
      }
    }
  }
  return cookieValue;
}

function showToast(message, isError = false) {
  const toast = document.getElementById("toast");
  toast.textContent = message;
  toast.style.backgroundColor = isError ? "#e74c3c" : "#2ecc71"; // red or green
  toast.className = "toast show";
  setTimeout(() => {  
    toast.className = "toast";
  }, 3000);
}

window.addEventListener('load', function() {
  console.log("base laoding")
  const navEntries = performance.getEntriesByType('navigation');
  if (navEntries.length > 0 && navEntries[0].type === 'reload') {
    console.log("yes relaoding")
    const pageKey = getPageStorageKey();
    if (pageKey){
      sessionStorage.removeItem(pageKey);
      console.log(`Removed sessionStorage key: ${pageKey}`);
      if (pageKey==='form-2-data' ) {
        console.log("deleting local storage also")
        localStorage.clear()
      }
    }
  }
});

function getPageStorageKey() {
  const path = window.location.pathname;
  if (path.includes('fill-custom-data')) return 'form-3-data';
  if (path.includes('fill-content-configuration')) return 'form-2-data';
  if (path.includes('home')) return 'form-1-data';
  return null;
}

const emojis = ["🕐", "🕜", "🕑","🕝", "🕒", "🕞", "🕓", "🕟", "🕔", "🕠", "🕕", "🕡", "🕖", "🕢",  "🕗", "🕣", "🕘", "🕤", "🕙",  "🕥", "🕚", "🕦",  "🕛", "🕧"];
const loadEmojis = (arr) => {
  const loader = document.getElementById('loader');
  if (loader) {
    const emoji = loader.querySelector('.emoji');
    const interval = 125;

    setInterval(() => {
      const randomIndex = Math.floor(Math.random() * arr.length);
      console.log("rn index", randomIndex)
      emoji.innerText = arr[randomIndex];
      console.log(emoji)
    }, interval);
  }
  else{
    console.log("noy loaded")
  }
}

const init = () => {
    loadEmojis(emojis);
  }