const express = require("express");
const app = express();
const path = require("path");
const { Storage } = require("@google-cloud/storage");
const Multer = require("multer");
const src = path.join(__dirname, "CSS-555-Project-Team-4");
app.use(express.static(src));

const multer = Multer({ //memory stream to express server to google cloud
  storage: Multer.memoryStorage(),
  limits: {
    fileSize: 10 * 1024 * 1024, // No larger than 10mb, malleable
  },
});

let projectId = "verdant-cascade-418002"; // From personal google cloud
let keyFilename = "TheKey.json"; // in files
const storage = new Storage({
  projectId,
  keyFilename,
});
const bucket = storage.bucket("eegbuc");

// Gets all files in the defined bucket
app.get("/upload", async (req, res) => {
    try {
      const [files] = await bucket.getFiles();
      res.send([files]);
      console.log("Success");
    } catch (error) {
      res.send("Error:" + error);
    }
  });

app.post("/upload", multer.single("up"), (req, res) => {
    console.log("Made it /upload");
    try {
        if (req.file) {
          console.log("File found, trying to upload...");
          const blob = bucket.file(req.file.originalname);
          const blobStream = blob.createWriteStream();

          blobStream.on("finish", () => {
            res.status(200).send("Success");
            console.log("Success");
        });
        blobStream.end(req.file.buffer);
    } else throw "error with file";
} catch (error) {
  res.status(500).send(error);
}
});

app.get("/", (req, res) => {
    res.sendFile(src + "/index.html");
  });