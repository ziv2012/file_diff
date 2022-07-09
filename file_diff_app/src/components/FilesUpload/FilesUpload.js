import React, { useState, useContext } from "react";
import { InboxOutlined } from "@ant-design/icons";
import { message, Button, Upload, Table } from "antd";
import TransContext from "../store/trans-context";
import "./FilesUpload.css";
import "antd/dist/antd.css";
const columns = [
  {
    title: "trans_id",
    dataIndex: "trans_id",
    key: "trans_id",
  },
  {
    title: "diff_type",
    dataIndex: "diff_type",
    key: "diff_type",
  },
  {
    title: "value_left",
    dataIndex: "value_left",
    key: "value_left",
  },
  {
    title: "value_right",
    dataIndex: "value_right",
    key: "value_right",
  },
];

const { Dragger } = Upload;
const FilesUpload = () => {
  const [files, setFiles] = useState([]);
  const transCtx = useContext(TransContext);

  const props = {
    name: "file",
    multiple: false,
    action: "https://www.mocky.io/v2/5cc8019d300000980a055e76",
    beforeUpload: (file) => {
      const isCSV = file.type === "text/csv";
      if (!isCSV) {
        message.error(`${file.name} is not a csv file`);
      } else if (files.length >= 2) {
        message.error(`can't upload another file - only 2 are allowed`);
        return false || Upload.LIST_IGNORE;
      } else {
        setFiles([...files, file]);
      }

      return isCSV || Upload.LIST_IGNORE;
    },
    onChange(info) {
      const { status } = info.file;

      if (status === "done") {
        message.success(`${info.file.name} file uploaded successfully.`);
      } else if (status === "error") {
        message.error(`${info.file.name} file upload failed.`);
      } else if (status === "removed") {
        removeFile(info.file.uid);
      }
    },
  };
  const removeFile = (uid) => {
    var array = files.filter(function (item) {
      return item.uid !== uid;
    });
    setFiles(array);
  };
  const onSubmit = async (e) => {
    e.preventDefault();
    if (files.length === 2) {
      const formData = new FormData();
      files.forEach((file) => {
        formData.append("files", file);
      });
      const requestOptions = {
        method: "POST",
        body: formData,
      };
      await fetch(process.env.REACT_APP_API_URL + "upload", requestOptions)
        .then((response) => {
          if (response.ok) {
            return response.json();
          }
          throw response;
        })
        .then((data) => {
          transCtx.onsetTransactions(data);
        })
        .catch((error) => {
          alert(error);
        });
    } else {
      alert("Please upload two files");
    }
  };

  return (
    <section id="table">
      {transCtx.transactions !== undefined && (
        <Table
          pagination={{ pageSize: 5 }}
          dataSource={transCtx.transactions}
          columns={columns}
        />
      )}

      <div className="upload_sections">
        <div className="dragger">
          <Dragger {...props}>
            <p className="ant-upload-drag-icon">
              <InboxOutlined />
            </p>
            <p className="ant-upload-text">
              Click or drag file to this area to upload
            </p>
          </Dragger>
        </div>
        <div className="dragger">
          <Dragger {...props}>
            <p className="ant-upload-drag-icon">
              <InboxOutlined />
            </p>
            <p className="ant-upload-text">
              Click or drag file to this area to upload
            </p>
          </Dragger>
        </div>
      </div>
      <div className="button">
        <Button type="primary" onClick={onSubmit}>
          Process
        </Button>
      </div>
    </section>
  );
};

export default FilesUpload;
