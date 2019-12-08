; sbcl 1.4.5
; sbcl --load day08.cl
; creates ./day08
(defun fread (fname)
  (let ((in (open fname :if-does-not-exist nil)))
    (when in
      (loop for line = (read-line in nil)
          while line do (format t "~a~%" line))
      (close in))))

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

(defun parse (s acc dim)
  ;(print "pin")
  ;(print (length s))
  ;(print acc)
  (if (= 0 (length s))
    (return-from parse (* (nth 1 acc) (nth 2 acc))))
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
      (return-from parse (parse rest (get-min acc cnh) dim)))))


(defun cli-args ()
  (or
    #+SBCL *posix-argv* nil))

(defun main ()
  (let ((args (cli-args)))
    (let ((fname (or (nth 1 args) "../input/day08/part1"))
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
  (print (parse data () dim))
  (print "")))))

(sb-ext:save-lisp-and-die "day08"
			  :executable t
			  :toplevel 'main)
