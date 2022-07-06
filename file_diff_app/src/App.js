import { InboxOutlined } from "@ant-design/icons";
import { message, Upload, Button, Table } from "antd";
import "antd/dist/antd.css";
import "./App.css";
import React, { useState } from "react";
const { Dragger } = Upload;
const BASE_URL = "http://localhost:8000/";

const App = () => {
  const [loadings, setLoadings] = useState([]);
  const [files, setFiles] = useState([]);
  const [result, setResult] = useState([]);

  const props = {
    name: "file",
    multiple: true,
    action: "https://www.mocky.io/v2/5cc8019d300000980a055e76",
    beforeUpload: (file) => {
      const isCSV = file.type === "text/csv";

      if (!isCSV) {
        message.error(`${file.name} is not a csv file`);
      } else {
        setFiles([...files, file]);
      }

      return isCSV || Upload.LIST_IGNORE;
    },
    onChange(info) {
      const { status } = info.file;

      if (status !== "uploading") {
        console.log(info.file, info.fileList);
      }

      if (status === "done") {
        message.success(`${info.file.name} file uploaded successfully.`);
      } else if (status === "error") {
        message.error(`${info.file.name} file upload failed.`);
      }
    },

    onDrop(e) {
      console.log("Dropped files", e.dataTransfer.files);
    },
  };

  const onSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    files.forEach((file) => {
      formData.append("files", file);
    });
    const requestOptions = {
      method: "POST",
      body: formData,
    };
    await fetch(BASE_URL + "upload", requestOptions)
      .then((response) => {
        if (response.ok) {
          return response.json();
        }
        throw response;
      })
      .then((data) => {
        debugger;
        console.log(data);
        setResult(data);
      });
  };

  const columns = [
    {
      title: "id",
      dataIndex: "id",
      key: "id",
    },
    {
      title: "diffType",
      dataIndex: "diffType",
      key: "diffType",
    },
    {
      title: "leftVal",
      dataIndex: "leftVal",
      key: "leftVal",
    },
    {
      title: "rightVal",
      dataIndex: "rightVal",
      key: "rightVal",
    },
  ];
  return (
    <>
      <section id="table">
        {result.length > 0 && <Table dataSource={result} columns={columns} />}
        <div className="upload_sections">
          <Dragger {...props}>
            <p className="ant-upload-drag-icon">
              <InboxOutlined />
            </p>
            <p className="ant-upload-text">
              Click or drag file to this area to upload
            </p>
            <p className="ant-upload-hint">
              Support for a single or bulk upload. Strictly prohibit from
              uploading company data or other band files
            </p>
          </Dragger>

          <Dragger {...props}>
            <p className="ant-upload-drag-icon">
              <InboxOutlined />
            </p>
            <p className="ant-upload-text">
              Click or drag file to this area to upload
            </p>
            <p className="ant-upload-hint">
              Support for a single or bulk upload. Strictly prohibit from
              uploading company data or other band files
            </p>
          </Dragger>
        </div>
        <div className="button">
          <Button type="primary" onClick={onSubmit}>
            Process
          </Button>
        </div>
      </section>
    </>
  );
};

export default App;
