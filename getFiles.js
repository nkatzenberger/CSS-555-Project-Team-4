import {getStorage, ref, listAll } from "firebase/storage";

/*
takes "user" as argument to determine from which database folder to pull filenames from
"DefaultUser is the value that should be passed to get some default files"
*/
function getFiles(user){
  const storage = getStorage();

  // Create a reference under which you want to list
  const listRef = ref(storage, 'files/uid/' + user);

  var files = [];
  
  // Find all the prefixes and items.
  listAll(listRef)
    .then((res) => {
      res.prefixes.forEach((folderRef) => {
        // All the prefixes under listRef.
        // You may call listAll() recursively on them.
      });
      res.items.forEach((itemRef) => {
        // All the items under listRef.
        files.push(itemRef);
      });
    }).catch((error) => {
      //error occurred
    });

    return files;
}

