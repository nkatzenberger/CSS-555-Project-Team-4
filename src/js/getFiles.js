import {getStorage, ref, listAll, getDownloadURL } from "https://www.gstatic.com/firebasejs/10.10.0/firebase-storage.js";
const storage = getStorage();
/*
takes "user" as argument to determine from which database folder to pull filenames from
"DefaultUser is the value that should be passed to get some default files"
*/
function getFiles(user) {
  console.log("getfiles initialized");
  

  const listRef = ref(storage, 'gs://eegdata-93ae1.appspot.com/' + user);

  return listAll(listRef)
      .then((res) => {
          const files = res.items.map(itemRef => itemRef.name); // Extract filenames
          console.log("files in folder:", files);
          return files;
      })
      .catch((error) => {
          console.error("error occurred:", error);
          throw error; // Propagate the error
      });
}

export default getFiles;