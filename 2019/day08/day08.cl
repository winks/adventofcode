; sbcl 1.4.5
; sbcl --load day08.cl
; creates ./day08
(defun file-string (path)
  (with-open-file (stream path)
   (let ((data (make-string (file-length stream))))
     (read-sequence data stream)
       data)))

(defun trim (s)
  (string-trim '(#\Space #\Newline #\Backspace #\Tab #\Linefeed #\Page #\Return #\Rubout) s))

(defun is0 (x) (string= "0" x))
(defun is1 (x) (string= "1" x))
(defun is2 (x) (string= "2" x))

(defun cnt (s)
  (list (length (remove-if-not #'is0 s))
        (length (remove-if-not #'is1 s))
        (length (remove-if-not #'is2 s))))

(defun get-min (l r)
  (let ((l2 (if l l '(9999 9999 9999)))
	(r2 (if r r '(9999 9999 9999))))
    (if (< (first l2) (first r2)) l2 r2)))

(defun parse1 (s acc dim)
  ;(print "pin")
  ;(print (length s))
  ;(print acc)
  (if (= 0 (length s))
    (return-from parse1 (* (nth 1 acc) (nth 2 acc))))
  (let ((head (subseq s 0 dim))
	(rest (subseq s dim)))
    ;(print "end")
    ;(print (length head))
    ;(print head)
    ;(print (length rest))
    ;(print rest)
    (let ((cnh (cnt head)))
      ;(print acc)
      ;(print cnh)
      (return-from parse1 (parse1 rest (get-min acc cnh) dim)))))

(defun ow (lower upper x)
  (if (= 0 (length lower))
    x
    (let ((a (if (string= "2" (subseq upper 0 1)) (subseq lower 0 1) (subseq upper 0 1))))
      (ow (subseq lower 1) (subseq upper 1) (concatenate 'string x a)))))

(defun parse2 (s acc dim)
  (if (= 0 (length s))
    (return-from parse2 acc))
  (let ((s1 (- (length s) dim)))
    (let ((tail (subseq s s1 (length s)))
	  (rest (subseq s 0 s1)))
    (return-from parse2 (parse2 rest (ow (if acc acc tail) tail "") dim)))))

(defun conv (s w acc)
  (if (= 0 (length s))
    (concatenate 'string '(#\linefeed) acc)
    (let ((x (if (string= "0" (subseq s 0 1)) "." "░"))
	  (y (if (or (= (- w 1) (length acc)) (and (> (length acc) 1) (= 1 (mod (length s) w)))) '(#\f #\linefeed) "")))
      (conv (subseq s 1) w (concatenate 'string acc x y)))))

(defun cli-args ()
  (or
    #+SBCL *posix-argv* nil))

(defun main ()
  (let ((args (cli-args)))
    (let ((fname (or (nth 1 args) "input.txt"))
	  (iw    (or (parse-integer (nth 2 args)) 2))
	  (ih    (or (parse-integer (nth 3 args)) 2)))
      (let ((data (trim (file-string fname)))
	    (dim (* iw ih)))
  ;(print args)
  (print fname)
  (print iw)
  (print ih)
  (print dim)
  (print "------------------------------")
  (print data)
  (print "------------------------------")
  (print (parse1 data () dim))
  (print "------------------------------")
  (let ((r2 (parse2 data () dim)))
    (print r2 )
    (print (conv r2 iw ""))
    (print ""))))))

(sb-ext:save-lisp-and-die "day08"
			  :executable t
			  :toplevel 'main)
