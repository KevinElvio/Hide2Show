<?php

namespace App\Http\Controllers;
use Illuminate\Support\Str;
use Illuminate\Http\Request;

class UploadFileController extends Controller
{
    public function uploadEncrypt(Request $request)
    {

        if ($request->file('file')) {
            $path = $request->file('file')->store('uploadEncrypt', 'public');

            return back()->with('success', 'File uploaded successfully.')->with('file', $path);
        }

        return back()->withErrors(['file' => 'Please upload a file.']);
    }
    public function uploadDecrypt(Request $request)
    {
        if ($request->file('file')) {
            $extension = $request->file('file')->getClientOriginalExtension();
            $filename = Str::slug($request->input('filename')) . '.' . $extension;
            $path = $request->file('file')->storeAs('uploadDecrypt', $filename, 'public');

            return back()->with('success', 'File uploaded successfully.')->with('file', $path);
        }

        return back()->withErrors(['file' => 'Please upload a file.']);
    }
}
