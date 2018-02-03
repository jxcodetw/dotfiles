

;; Added by Package.el.  This must come before configurations of
;; installed packages.  Don't delete this line.  If you don't want it,
;; just comment it out by adding a semicolon to the start of the line.
;; You may delete these explanatory comments.
(package-initialize)

(load-file (let ((coding-system-for-read 'utf-8))
                (shell-command-to-string "agda-mode locate")))
(put 'downcase-region 'disabled nil)

(set-face-attribute 'default nil :family "Consolas")
(set-face-attribute 'default nil :height 200)

(tool-bar-mode -1)

(setq make-backup-files nil)
