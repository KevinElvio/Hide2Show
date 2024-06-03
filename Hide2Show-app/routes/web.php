<?php

use App\Http\Controllers\UploadFileController;
use Illuminate\Support\Facades\Route;

Route::get('/', function () {
    return view('encrypt');
});
Route::get('/encrypt', function () {
    return view('encrypt');
});
Route::get('/decrypt', function () {
    return view('decrypt');
});
Route::post('/uploadEncrypt', [UploadFileController::class, 'uploadEncrypt'])->name('file.uploadEncrypt');
Route::post('/uploadDecrypt', [UploadFileController::class, 'uploadDecrypt'])->name('file.uploadDecrypt');
