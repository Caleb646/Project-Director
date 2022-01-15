import React, { useState } from "react";

import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  TableContainer,
  Grid,
  Typography,
  Paper,
  Button,
  Theme,
  makeStyles,
  AppBar,
  Box,
  Collapse,
  Divider,
  IconButton,
  Toolbar,
  Drawer,
  List,
  ListItem,
  ListItemText,
  responsiveFontSizes,
} from "@material-ui/core";

import MenuIcon from "@material-ui/icons/Menu";

import {
  useFetch,
  ApiClient,
  useAuth,
  CollapsibleTblRow,
  useAuthContext,
  fPaths,
  Header,
  Link,
  apiPaths,
  FilterForm,
  CreateUserForm,
  getKey,

  //types
  dataTypes,
} from "../../src";
interface rfiTableProps {
  setRFIUrl: React.Dispatch<React.SetStateAction<string>>;
  currentRFIUrl: string;
}

const rfiTableStyles = makeStyles((theme: Theme) => ({
  menuButton: {
    marginRight: theme.spacing(2),
  },
  title: {
    flexGrow: 1,
  },

  appBar: {
    Color: theme.palette.primary,
  },

  tableContainer: {
    maxHeight: 440,
  },
}));

const RFITableSection: React.FC<rfiTableProps> = ({
  currentRFIUrl,
  setRFIUrl,
}) => {
  const classes = rfiTableStyles();
  const {
    data: rfis,
    loading: rfisLoading,
    error: rfiError,
  } = useFetch<dataTypes.RFIList>(currentRFIUrl);

  const filters = [
    {
      title: "Date Created",
      name: "date_created__date__gte",
      options: [
        {
          title: "30 Days Ago",
          value: thirty,
        },
        {
          title: "60 Days Ago",
          value: sixty,
        },

        {
          title: "90 Days Ago",
          value: ninety,
        },
      ],
    },
  ];

  const onFilterSubmit = (filterValues: {}) => {
    let queryParams = "";
    Object.entries(filterValues).map((kV) => {
      if (kV[1] === undefined || kV[1] === null || kV[1] === "") return;
      queryParams += `${kV[0]}=${kV[1]}`;
    });
    if (!currentRFIUrl.includes("?")) {
      setRFIUrl(currentRFIUrl + "?" + queryParams);
      return;
    }
    setRFIUrl(currentRFIUrl + "&" + queryParams);
  };

  const paginate = (url: string | null | undefined) => {
    if (url === null || url === undefined) return;
    setRFIUrl(url);
  };
  return (
    <>
      <Grid item xs={12}>
        <AppBar className={classes.appBar} position="static">
          <Toolbar>
            <IconButton
              edge="start"
              className={classes.menuButton}
              color="inherit"
              aria-label="menu"
            >
              <MenuIcon />
            </IconButton>
            <Typography variant="h6" className={classes.title}>
              RFIs
            </Typography>
            <FilterForm filters={filters} onSubmit={onFilterSubmit} />
          </Toolbar>
        </AppBar>
      </Grid>
      <Grid item xs={12}>
        <TableContainer className={classes.tableContainer}>
          <Table aria-label="collapsible table">
            <TableHead>
              <TableRow>
                <TableCell>Details</TableCell>
                <TableCell>From</TableCell>
                <TableCell>Subject</TableCell>
                <TableCell>Date Created</TableCell>
                <TableCell>
                  <Button onClick={() => paginate(rfis.previous)}>&lt;</Button>
                  <Button onClick={() => paginate(rfis.next)}>&gt;</Button>
                </TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {rfis.results.map((rfi: dataTypes.BaseRFI) => {
                return (
                  <CollapsibleTblRow
                    key={getKey()}
                    mainRow={[
                      rfi.f_user.email,
                      rfi.subject,
                      new Date(rfi.date_created).toLocaleString(),
                    ]}
                    subColumn={["CC'd Users"]}
                    subRow={rfi.t_user.map(
                      (user: dataTypes.BaseUser) => user.email
                    )}
                  />
                );
              })}
            </TableBody>
          </Table>
        </TableContainer>
      </Grid>
    </>
  );
};

interface userTableProps {
  setUserUrl: React.Dispatch<React.SetStateAction<string>>;
  currentUserUrl: string;
}

const userTableStyles = makeStyles((theme: Theme) => ({
  menuButton: {
    marginRight: theme.spacing(2),
  },
  title: {
    flexGrow: 1,
  },

  appBar: {
    Color: theme.palette.primary,
  },

  tableContainer: {
    maxHeight: 440,
  },
}));

const UserTableSection: React.FC<userTableProps> = ({
  setUserUrl,
  currentUserUrl,
}) => {
  const classes = userTableStyles();
  const {
    data: users,
    loading: usersLoading,
    error: userError,
  } = useFetch<dataTypes.UserList>(currentUserUrl);
  console.log("users: ", users);
  const filters = [
    {
      title: "Date Created",
      name: "date_created__date__gte",
      options: [
        {
          title: "30 Days Ago",
          value: thirty,
        },
        {
          title: "60 Days Ago",
          value: sixty,
        },

        {
          title: "90 Days Ago",
          value: ninety,
        },
      ],
    },
  ];

  const onFilterSubmit = (filterValues: {}) => {
    let queryParams = "";
    Object.entries(filterValues).map((kV) => {
      if (kV[1] === undefined || kV[1] === null || kV[1] === "") return;
      queryParams += `${kV[0]}=${kV[1]}`;
    });
    if (!currentUserUrl.includes("?")) {
      setUserUrl(currentUserUrl + "?" + queryParams);
      return;
    }
    setUserUrl(currentUserUrl + "&" + queryParams);
  };

  const paginate = (url: string | null | undefined) => {
    if (url === null || url === undefined) return;
    setUserUrl(url);
  };
  return (
    <>
      <Grid item xs={12}>
        <AppBar className={classes.appBar} position="static">
          <Toolbar>
            <IconButton
              edge="start"
              className={classes.menuButton}
              color="inherit"
              aria-label="menu"
            >
              <MenuIcon />
            </IconButton>
            <Typography variant="h6" className={classes.title}>
              Users
            </Typography>
            <CreateUserForm createOrUpdate="create" />
            <FilterForm filters={filters} onSubmit={onFilterSubmit} />
          </Toolbar>
        </AppBar>
      </Grid>
      <Grid item xs={12}>
        <TableContainer className={classes.tableContainer}>
          <Table aria-label="collapsible table">
            <TableHead>
              <TableRow>
                <TableCell>Details</TableCell>
                <TableCell>Email</TableCell>
                <TableCell>Active</TableCell>
                <TableCell>Admin</TableCell>
                <TableCell>Edit</TableCell>
                {/* <TableCell>
                  <Button onClick={() => paginate(users.previous)}>&lt;</Button>
                  <Button onClick={() => paginate(users.next)}>&gt;</Button>
                </TableCell> */}
              </TableRow>
            </TableHead>
            <TableBody>
              {users.results.map((user: dataTypes.DetailedUser) => {
                return (
                  <CollapsibleTblRow
                    key={getKey()}
                    mainRow={[
                      user.email,
                      user.is_active ? "yes" : "no",
                      user.is_staff ? "yes" : "no",
                      <CreateUserForm
                        createOrUpdate="update"
                        userId={user.id}
                      />,
                      //new Date(rfi.date_created).toLocaleString(),
                    ]}
                    subColumn={["Groups"]}
                    subRow={user.groups.map(
                      (group: dataTypes.Group) => group.name
                    )}
                  />
                );
              })}
            </TableBody>
          </Table>
        </TableContainer>
      </Grid>
    </>
  );
};

interface Props {}

const useStyles = makeStyles((theme: Theme) => ({
  root: {
    flexGrow: 1,
    zIndex: 1,
    overflow: "hidden",
    position: "relative",
    display: "flex",
  },
  menuButton: {
    marginRight: theme.spacing(2),
  },
  title: {
    flexGrow: 1,
  },
  drawerPaper: {
    position: "relative",
    width: 240,
  },
  content: {
    flexGrow: 1,
    backgroundColor: theme.palette.background.default,
    padding: theme.spacing.length * 3, //TODO no idea what this does
    minWidth: 0, // So the Typography noWrap works
  },
  tableContainer: {
    maxHeight: 440,
  },
  toolbar: theme.mixins.toolbar,
}));

let thirty = new Date();
thirty.setDate(thirty.getDate() - 30).toString();
let sixty = new Date();
sixty.setDate(sixty.getDate() - 60).toString();
let ninety = new Date();
ninety.setDate(ninety.getDate() - 90).toString();

const PmHome: React.FC<Props> = () => {
  const classes = useStyles();

  const authUser: void = useAuth(false, "", null);
  //const { user } = useAuthContext();

  //this allows for the url to be changed with the click of a button and
  //the rfi data to be fetched with the new parameters.
  const [currentRFIUrl, setcurrentRFIUrl] = useState(apiPaths.allRfis);
  const [currentUserUrl, setCurrentUserUrl] = useState(apiPaths.allUsers);
  const {
    data: jobs,
    loading: jobsLoading,
    error: jobsError,
  } = useFetch<dataTypes.JobList>(apiPaths.jobs);

  const rfiSectionProps = {
    setRFIUrl: setcurrentRFIUrl,
    currentRFIUrl: currentRFIUrl,
  };

  const userSectionProps = {
    setUserUrl: setCurrentUserUrl,
    currentUserUrl: currentUserUrl,
  };

  const links = [
    {
      path: apiPaths.logout,
      title: "Logout",
    },
  ];

  const filterByJob = (jobId: number | null) => {
    if (jobId === null) {
      setcurrentRFIUrl(apiPaths.allRfis);
      setCurrentUserUrl(apiPaths.allUsers);
      return;
    }

    setcurrentRFIUrl(apiPaths.rfisByJob(jobId));
    setCurrentUserUrl(apiPaths.usersByJob(jobId));
  };

  return (
    <>
      <Header links={links} title={"User Job Name Here"} />
      <div>
        <div className={classes.root}>
          <Drawer
            variant="permanent"
            classes={{
              paper: classes.drawerPaper,
            }}
          >
            <List>
              <ListItem key={getKey()} onClick={() => filterByJob(null)} button>
                <ListItemText key={getKey()} primary="All Jobs" />
              </ListItem>
              <Divider />
              {jobs.results.map((job: dataTypes.BaseJob) => {
                return (
                  <>
                    <ListItem
                      key={getKey()}
                      onClick={() => filterByJob(job.id)}
                      button
                    >
                      <ListItemText key={getKey()} primary={job.name} />
                    </ListItem>
                  </>
                );
              })}
            </List>
          </Drawer>

          <Grid container spacing={3}>
            <UserTableSection {...userSectionProps} />
            <RFITableSection {...rfiSectionProps} />
          </Grid>
        </div>
      </div>
    </>
  );
};

export default PmHome;
