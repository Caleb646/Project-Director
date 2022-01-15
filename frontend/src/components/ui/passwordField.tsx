import React, { useState } from "react";

import { InputAdornment } from "@material-ui/core";
import TextField from "@material-ui/core/TextField";
import { RemoveRedEye } from "@material-ui/icons";

interface Props {}

export const PasswordField: React.FC<Props> = () => {
  const [masked, setMasked] = useState<boolean>(true);

  return (
    <TextField
      required
      fullWidth
      type={masked ? "password" : "text"}
      variant="outlined"
      name="password"
      autoComplete="on"
      label="Password"
      InputProps={{
        endAdornment: (
          <InputAdornment position="end">
            <RemoveRedEye onClick={() => setMasked(!masked)} />
          </InputAdornment>
        ),
      }}
    />
  );
};
