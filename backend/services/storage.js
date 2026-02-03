const AWS = require('aws-sdk');

// Configure AWS
AWS.config.update({
  accessKeyId: process.env.AWS_ACCESS_KEY_ID,
  secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY,
  region: process.env.AWS_REGION || 'us-east-1'
});

const s3 = new AWS.S3();

class StorageService {
  constructor() {
    this.bucket = process.env.S3_BUCKET_NAME;
    this.cdnUrl = process.env.CDN_URL;
    this.maxFileSize = parseInt(process.env.MAX_UPLOAD_SIZE || '10485760');
  }

  async uploadFile(file, key) {
    const params = {
      Bucket: this.bucket,
      Key: key,
      Body: file,
      ACL: process.env.S3_ACL || 'private',
      ServerSideEncryption: process.env.S3_ENCRYPTION || 'AES256'
    };

    return await s3.upload(params).promise();
  }

  async deleteFile(key) {
    const params = {
      Bucket: this.bucket,
      Key: key
    };

    return await s3.deleteObject(params).promise();
  }

  getSignedUrl(key, expiresIn = 3600) {
    return s3.getSignedUrl('getObject', {
      Bucket: this.bucket,
      Key: key,
      Expires: expiresIn
    });
  }
}

module.exports = StorageService;
