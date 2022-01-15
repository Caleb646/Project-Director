//@ts-nocheck
import React, { useEffect, useState } from "react";

import {
  Modal,
  makeStyles,
  Theme,
  createStyles,
  Grid,
  TextField,
  InputLabel,
  FormControl,
  Select,
  MenuItem,
  Checkbox,
  ListItemText,
  Input,
  Button,
  Container,
} from "@material-ui/core";

import AddBoxIcon from "@material-ui/icons/AddBox";

import axios, { AxiosRequestConfig } from "axios";

import { useFetch, useAuthContext } from "../../hooks";
import { apiPaths } from "../nav";
import { ApiClient } from "../../services";
import { dataTypes } from "../../types";

const HEIGHT = 350;
const WIDTH = 400;

const useStyles = makeStyles((theme: Theme) =>
  createStyles({
    container: {
      color: "black",
    },
    formControl: {
      margin: theme.spacing(1),
      minWidth: 120,
    },

    paper: {
      top: "center",
      left: "center",
      position: "absolute",
      width: WIDTH,
      height: HEIGHT,
      backgroundColor: theme.palette.background.paper,
      border: "2px solid #000",
      boxShadow: theme.shadows[5],
      padding: theme.spacing(2, 4, 3),
    },
  })
);

const ITEM_HEIGHT = 48;
const ITEM_PADDING_TOP = 8;
const MenuProps = {
  PaperProps: {
    style: {
      maxHeight: ITEM_HEIGHT * 4.5 + ITEM_PADDING_TOP,
      width: 250,
    },
  },
};

interface Props {
  createOrUpdate: "create" | "update";
  userId?: number | string;
}

export const CreateUserForm: React.FC<Props> = ({ createOrUpdate, userId }) => {
  const classes = useStyles();
  const [open, setOpen] = useState(false);

  const { getToken } = useAuthContext();

  const {
    data: jobs,
    loading: jobsLoading,
    error: jobsError,
  } = useFetch<dataTypes.JobList>(apiPaths.jobs, open);

  //if update is chosen and the modal is open then get the specified user.
  const {
    data: userInfo,
    loading: userInfoLoading,
    error: userInfoError,
  } = useFetch<dataTypes.UserDetail>(
    apiPaths.usersById(userId as number),
    createOrUpdate === "update" && open
  );

  const {
    data: groups,
    loading: groupsLoading,
    error: groupsError,
  } = useFetch<dataTypes.GroupList>(apiPaths.allGroups, open);

  const [formState, setFormState] = useState({
    first_name: "",
    last_name: "",
    email: "",
    job_set: [],
    groups: "",
  });

  const setState = () => {
    /*
      if update is chosen update each field with users current information.
      */

    if (userInfo.results.length === 0) return;
    const info = userInfo.results[0];
    setFormState({
      first_name: info.first_name || "",
      last_name: info.last_name || "",
      email: info.email || "",
      job_set: info.job_set.map((job: dataTypes.BaseJob) => job.id) || [],
      groups: info.groups.map((group: dataTypes.Group) => group.id)[0] || "",
    });
  };

  const handleOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  const handleChange = (
    e: React.ChangeEvent<{ name?: string | undefined; value: string }>
  ) => {
    //console.log("handling change: ", e.target.name, e.target.value);
    console.assert(
      e.target.name !== undefined,
      "e.target.name has to be defined!!!"
    );
    setFormState({
      ...formState,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = (e: any) => {
    e.preventDefault();
    if (createOrUpdate === "create") createUser();
    else updateUser();
  };

  const createUser = async () => {
    const signal = axios.CancelToken.source();
    const accessToken = await getToken(signal);

    const config: AxiosRequestConfig = {
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    };
    ApiClient.post(apiPaths.userCreateInvite, formState, config)
      .then((response) => console.log("created user", response))
      .catch((error) =>
        console.log("user could not be created because: ", error)
      );
  };

  const updateUser = async () => {
    const signal = axios.CancelToken.source();
    const accessToken = await getToken(signal);

    const config: AxiosRequestConfig = {
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    };
    ApiClient.patch(apiPaths.userUpdate(userId as number), formState, config)
      .then((response) => console.log("updated user", response))
      .catch((error) =>
        console.log("user could not be created because: ", error.response)
      );
  };

  //if update is chosen then set the user to be updated info in the
  //right fields.
  useEffect(() => {
    console.log("loading user info.");
    setState();
  }, [userInfoLoading]);

  return (
    <div>
      {createOrUpdate === "create" ? (
        <Button variant="contained" color="secondary" onClick={handleOpen}>
          <AddBoxIcon />
        </Button>
      ) : (
        <Button variant="outlined" onClick={handleOpen}>
          <AddBoxIcon />
        </Button>
      )}
      <Modal open={open} onClose={handleClose}>
        <Container className={classes.paper}>
          <form>
            <Grid container spacing={3}>
              <Grid item xs={6}>
                <TextField
                  id="outlined-basic"
                  label="First Name"
                  name="first_name"
                  value={formState.first_name}
                  onChange={handleChange}
                  variant="outlined"
                  required={true}
                />
              </Grid>
              <Grid item xs={6}>
                <TextField
                  id="outlined-basic"
                  label="Last Name"
                  name="last_name"
                  value={formState.last_name}
                  onChange={handleChange}
                  variant="outlined"
                  required={true}
                />
              </Grid>

              <Grid flex item xs={12}>
                <TextField
                  id="outlined-basic"
                  label="Email"
                  name="email"
                  value={formState.email}
                  onChange={handleChange}
                  variant="outlined"
                  required={true}
                />
              </Grid>

              <Grid item xs={6}>
                <FormControl className={classes.formControl}>
                  <InputLabel>Jobs</InputLabel>
                  <Select
                    multiple
                    value={formState.job_set}
                    name="job_set"
                    onChange={handleChange}
                    input={<Input />}
                    renderValue={(selected) => (selected as unknown).join(", ")}
                    MenuProps={MenuProps}
                  >
                    {jobs.results.map((job: dataTypes.BaseJob) => (
                      <MenuItem key={job.id} value={job.id}>
                        <Checkbox
                          checked={formState.job_set.indexOf(job.id) > -1}
                        />
                        <ListItemText primary={job.name} />
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>

              <Grid item xs={6}>
                <FormControl className={classes.formControl}>
                  <InputLabel>Group</InputLabel>
                  <Select
                    value={formState.groups}
                    onChange={handleChange}
                    name="groups"
                    input={<Input />}
                    MenuProps={MenuProps}
                  >
                    {groups.results.map((group: dataTypes.Group) => (
                      <MenuItem key={group.id} value={group.id}>
                        <ListItemText primary={group.name} />
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>

              <Grid flex item xs={6}>
                <FormControl className={classes.formControl}>
                  <Button
                    variant="contained"
                    color="secondary"
                    onClick={handleClose}
                  >
                    Cancel
                  </Button>
                </FormControl>
              </Grid>

              <Grid flex item xs={6}>
                <FormControl className={classes.formControl}>
                  <Button
                    variant="contained"
                    color="secondary"
                    onClick={handleSubmit}
                  >
                    {createOrUpdate}
                  </Button>
                </FormControl>
              </Grid>
            </Grid>
          </form>
        </Container>
      </Modal>
    </div>
  );
};
