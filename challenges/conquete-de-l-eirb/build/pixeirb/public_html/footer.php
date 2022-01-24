<footer>
    <div class="copyright">
        <p>
            Fait avec
            <ion-icon name="heart"></ion-icon>
            par Antoine Boulangé, Juliette Deguillaume et Florian Mornet !
        </p>
        <p>
            Avec l'accord du club, le site a été modifié par @Kobh4x, @LePlanCity et @Erak.
        </p>
        <p>
            Copyright PixEirb &copy;<?php echo date("Y"); ?>. Tous droits réservés. Inspiré par <a
                    href="https://colorlib.com" target="_blank">Colorlib</a>.
        </p>
    </div>

    <ul class="social-icons">
        <li><a target="_blank" href=#>
                <ion-icon name="logo-facebook"></ion-icon>
            </a></li>
        <li><a target="_blank" href=#>
                <ion-icon name="logo-instagram"></ion-icon>
            </a></li>
    </ul><!-- social-icons -->
</footer>

<!-- SCRIPTS -->
<script
        src="https://code.jquery.com/jquery-3.4.1.min.js"
        integrity="sha256-CSXorXvZcTkaix6Yvo6HppcZGetbYMGWSFlBw8HfCJo="
        crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js"
        integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1"
        crossorigin="anonymous"></script>
<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js"
        integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM"
        crossorigin="anonymous"></script>
<script type="module" src="https://unpkg.com/ionicons@4.5.10-0/dist/ionicons/ionicons.esm.js"></script>
<script nomodule="" src="https://unpkg.com/ionicons@4.5.10-0/dist/ionicons/ionicons.js"></script>
<?php if (basename($_SERVER['SCRIPT_NAME']) == 'index.php') { ?>
    <!-- REVOLUTION JS FILES -->
    <script type="text/javascript" src="/revolution/js/jquery.themepunch.tools.min.js"></script>
    <script type="text/javascript" src="/revolution/js/jquery.themepunch.revolution.min.js"></script>
<?php } ?>
<?php if (basename($_SERVER['SCRIPT_NAME']) == 'album.php') { ?>
    <!-- GALLERY -->
    <script src="https://unpkg.com/imagesloaded@4/imagesloaded.pkgd.min.js"></script>
    <script src="https://unpkg.com/isotope-layout@3/dist/isotope.pkgd.min.js"></script>
    <script src="https://cdn.jsdelivr.net/gh/fancyapps/fancybox@3.5.7/dist/jquery.fancybox.min.js"></script>
<?php } ?>

<script src="/js/scripts.js"></script>