import { Buffer } from 'buffer'

const { createCipheriv, createDecipheriv, randomBytes, createHash } = require('crypto');

const AES_BLOCK_SIZE = 16;
const HASH_ALGORITHM = 'sha256'
const CIPHER_ALGORITHM = 'aes-256-cbc';

function pad(s, blockSize=AES_BLOCK_SIZE) {
    const padding = String.fromCharCode(blockSize - s.length % blockSize).repeat(blockSize - s.length % blockSize);
    return Buffer.concat([s, Buffer.from(padding)]);
}

function unpad(s) {
    const lastElement = s.slice(s.length-1, s.length).toString();
    const rawLen = s.length - lastElement.charCodeAt();
    return s.slice(0, rawLen);
}

export function encrypt(raw, key) {
    if (raw === "") return raw;
    const keyBuffer = Buffer.from(key);
    const rawBuffer = Buffer.from(raw, 'utf8');
    const iv = randomBytes(AES_BLOCK_SIZE);
    console.log('encrypt');
    const hashedKeyBuffer = createHash(HASH_ALGORITHM).update(keyBuffer).digest();
    const encryptor = createCipheriv(CIPHER_ALGORITHM, hashedKeyBuffer, iv);
    encryptor.setAutoPadding(false);
    const paddedRaw = pad(rawBuffer);
    const cipherBuffer = Buffer.concat([encryptor.update(paddedRaw), encryptor.final()]);
    const finalBuffer = Buffer.concat([iv, cipherBuffer]);
    return finalBuffer.toString('base64');
}

export function decrypt(cipher, key) {
    if (cipher === "") return cipher;
    const keyBuffer = Buffer.from(key);
    const cipherBuffer = Buffer.from(cipher, 'base64');
    const iv = cipherBuffer.slice(0, AES_BLOCK_SIZE);
    console.log('decrypt');
    const hashedKeyBuffer = createHash(HASH_ALGORITHM).update(keyBuffer).digest();
    const decryptor = createDecipheriv(CIPHER_ALGORITHM, hashedKeyBuffer, iv);
    decryptor.setAutoPadding(false);
    const rawBuffer = Buffer.concat([decryptor.update(cipherBuffer.slice(AES_BLOCK_SIZE)), decryptor.final()]);
    const unpaddedRawBuffer = unpad(rawBuffer.toString('utf8'));
    return unpaddedRawBuffer;
}