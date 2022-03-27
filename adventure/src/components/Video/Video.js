import React, { useEffect, useState } from 'react'
import axios from 'axios'
import { Button, Form, Row, Col, Container, Modal, Fade } from 'react-bootstrap'
import ReactPlayer from "react-player";
import { VideoUrlBase, VideoPostUrl, VideoDisplayUrl, VideoDeleteUrl } from '../config'

import { FileActionHandler, setChonkyDefaults, FullFileBrowser, ChonkyActions } from 'chonky';

import { ChonkyIconFA } from 'chonky-icon-fontawesome';
setChonkyDefaults({ iconComponent: ChonkyIconFA });


function Video() {
  const [vidList, setvidList] = useState(null);
  const [currModal, setModal] = useState(null);

  function postVid(event) {
    event.preventDefault()
    var formData = new FormData();
    formData.append("file", event.target.elements.vidfile.files[0]);
    axios
      .post(VideoPostUrl, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
          Authorization: `Bearer ${localStorage.getItem('token')}`
        }
    })
    .then((response) => {
      setvidList(prevState => ([
        {
          id:response.data.filename,
          name:response.data.filename, 
          thumbnailUrl:`${VideoDisplayUrl}${response.data.thumbnail}`
        }, 
        ...prevState]
      ));
      setModal(null);
    });
  }

  function deleteVid(fname : string) {
    axios
      .post(`${VideoDeleteUrl}${fname}`, {}, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`
        }
    })
    .then((response) => {
      setvidList(prevState => (prevState.filter(vidFile => vidFile['name'] !== response.data['fname'] )));
    })
    .catch(error => {
      setModal({title:'Error', content:error.response.data});
    });
  }

  function getVids() {
    axios
      .get(VideoUrlBase, 
          { headers: 
            { Authorization: `Bearer ${localStorage.getItem('token')}` }
          })
      .then((response) => {
        const files = response.data
          ? response.data.map((vidFile) => {
            return {
              id:vidFile['filename'],
              name:vidFile['filename'],
              thumbnailUrl:`${VideoUrlBase}/display/${vidFile['thumbnail']}`
            }
          })
          : [];
        setvidList(files);
      })
      .catch(error => {
        setvidList(null);
    });
  }

  function MainModal(props) {
    return (
      currModal ?
      <Modal
        {...props}
        size="lg"
        aria-labelledby="contained-modal-title-vcenter"
        centered
      >
        <Modal.Header closeButton>
          <Modal.Title id="contained-modal-title-vcenter">
            {currModal.title}
          </Modal.Title>
        </Modal.Header>
        <Modal.Body>
          {currModal.content}
        </Modal.Body>
        <Modal.Footer>
          <Button onClick={props.onHide}>Close</Button>
        </Modal.Footer>
      </Modal>
    : null
    );
  }

  useEffect(getVids, []);

  function showPlayer(fname) {
    return (
      <ReactPlayer url={`${VideoDisplayUrl}${fname}`} width="100%" height="100%" controls={true} />
    )
  }

  const handleAction: FileActionHandler = (data) => {
    if (data.id === ChonkyActions.OpenFiles.id) {
      setModal(() => ({
        title:data.payload.targetFile['name'],
        content:<ReactPlayer url={`${VideoDisplayUrl}${data.payload.targetFile['name']}`} width="100%" height="100%" controls={true} />
      }));
    } else if (data.id === ChonkyActions.DeleteFiles.id) {
      data.state.selectedFilesForAction.map((vidFile) => {
        deleteVid(vidFile['name']);
      });
    } else if (data.id === ChonkyActions.UploadFiles.id) {
      setModal(() => ({
        title:'Upload New Video',
        content:
           <Form onSubmit={postVid}>
             <Form.Group>
               <Form.File id="vidfile" label="Upload new Video" />
             </Form.Group>
             <Form.Group>
                 <Button type="submit">Upload New</Button>
             </Form.Group>
           </Form>
      }));
    }
    // add rename
    // add download
  };

  const actionsToDisable: string[] = [
    ChonkyActions.SelectAllFiles.id,
  ];

  const actionsToEnable = [
      ChonkyActions.UploadFiles,
      ChonkyActions.DownloadFiles,
      ChonkyActions.DeleteFiles,
  ];

  return (
    <div>
    <Fade appear={true} in={true}>
    <div>
      <Container>
          <FullFileBrowser 
            files={vidList} 
            onFileAction={handleAction} 
            disableDefaultFileActions={actionsToDisable} 
            fileActions={actionsToEnable}
          />
      </Container>
      <MainModal
        show={currModal ? true : false}
        onHide={() => setModal(null)}
      />

    </div>
    </Fade>
    </div>
  );
};


export default Video;

