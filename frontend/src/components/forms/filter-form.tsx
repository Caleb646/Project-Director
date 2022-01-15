//@ts-nocheck

import React, { useState } from "react";

import {
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  Input,
  InputLabel,
  MenuItem,
  FormControl,
  Select,
  Theme,
  createStyles,
  makeStyles,
} from "@material-ui/core";

import { Filter } from "@material-ui/icons";

import { getKey } from "../../utils";

const useStyles = makeStyles((theme: Theme) =>
  createStyles({
    container: {
      color: "black",
      display: "flex",
      flexWrap: "wrap",
    },
    formControl: {
      margin: theme.spacing(1),
      minWidth: 120,
    },

    filterIcon: {
      Color: theme.palette.secondary,
    },
  })
);

type options = {
  value: string | number | Date;
  title: string;
};
type filter = {
  title: string;
  name: string;
  options: Array<options>;
};

interface Props {
  onSubmit: (filterValues: any) => void;
  filters: Array<filter>;
}

export const FilterForm: React.FC<Props> = ({ filters, onSubmit }) => {
  const classes = useStyles();
  const [open, setOpen] = useState(false);
  //create state from filter names
  const [filterState, setFilterState] = useState(
    filters.reduce((o, filter) => ({ ...o, [filter.name]: undefined }), {})
  );

  //console.log("current state: ", filterState);

  const handleSubmit = () => {
    setOpen(false);
    //console.log("select names", JSON.stringify(filterState));
    onSubmit(filterState);
  };

  const handleChange = (event: React.ChangeEvent<{ value: unknown }>) => {
    setFilterState({
      ...filterState,
      [event.target.name]: event.target.value,
    });
  };

  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  return (
    <div>
      <Button variant="contained" color="secondary" onClick={handleClickOpen}>
        <Filter />
      </Button>
      <Dialog disableEscapeKeyDown open={open} onClose={handleClose}>
        {/* <DialogTitle>Fill the form</DialogTitle> */}
        <DialogContent>
          <form className={classes.container}>
            {filters.map((filter) => {
              return (
                <FormControl key={getKey()} className={classes.formControl}>
                  <InputLabel key={getKey()}>{filter.title}</InputLabel>
                  <Select
                    key={getKey()}
                    name={filter.name}
                    onChange={handleChange}
                    value={filterState[filter.name]}
                    input={<Input />}
                  >
                    <MenuItem key={getKey()} value={undefined}>
                      <em>None</em>
                    </MenuItem>
                    {filter.options.map((option) => {
                      return (
                        <MenuItem key={getKey()} value={option.value}>
                          {option.title}
                        </MenuItem>
                      );
                    })}
                  </Select>
                </FormControl>
              );
            })}
          </form>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose} color="primary">
            Cancel
          </Button>
          <Button onClick={handleSubmit} color="primary">
            Ok
          </Button>
        </DialogActions>
      </Dialog>
    </div>
  );
};
