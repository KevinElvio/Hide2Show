@extends('layouts.app')

@section('content')
    <div class="d-flex justify-content-evenly mt-5">
        <h1 class="fw-bold">Encrypt</h1>
        <h1 class="fw-bold">Decrypt</h1>
    </div>
    <div class="input-group mb-3 mt-5 ml-5">
        <label class="input-group-text" for="inputGroupFile01">Upload</label>
        <input type="file" class="form-control" id="inputGroupFile01">
    </div>
@endsection
