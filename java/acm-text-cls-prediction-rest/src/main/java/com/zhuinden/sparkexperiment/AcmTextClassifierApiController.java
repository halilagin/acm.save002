package com.zhuinden.sparkexperiment;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import com.zhuinden.sparkexperiment.AcmTextClassifier;
import java.util.List;

/**
 * Created by Owner on 2017. 03. 29..
 */
@RequestMapping("api")
@Controller
public class AcmTextClassifierApiController {
    @Autowired
    AcmTextClassifier textClassifier;

    @RequestMapping("textcls")
    public ResponseEntity<String> predict() {
        return new ResponseEntity<>(textClassifier.predict(), HttpStatus.OK);
    }
}
