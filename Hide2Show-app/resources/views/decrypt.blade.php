@extends('layouts.app')

@section('content')
<style>
  .navbar-nav {
    display: flex;
    justify-content: space-evenly;
    width: 100%;
  }
</style>
<nav class="navbar navbar-expand-md bg-dark navbar-dark">
  <div class="container-fluid">
    <ul class="navbar-nav">
      <li class="nav-item">
        <a class="nav-link" href="/encrypt">Encrypt</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="/decrypt">Decrypt</a>
      </li>
    </ul>
  </div>
</nav>
<form action="{{ route('file.uploadDecrypt') }}" method="POST" enctype="multipart/form-data">
  @csrf
  <div class="container d-flex flex-column ">
    <div class="row">
      <div class="input-group mb-3 mt-5">
        <label class="input-group-text" for="inputGroupFile01">Upload</label>
        <input type="file" name="file" class="form-control" id="inputGroupFile01">
      </div>
    </div>
    <div class="row">
      <div class="input-group mb-3">
        <label class="input-group-text" for="inputGroupFile02">Text</label>
        <input type="text" name="filename" class="form-control" id="inputGroupFile02">
      </div>
    </div>
    <button type="submit" class="btn btn-success">Simpan dan Deskripsi</button>
  </div>
</form>
@endsection
