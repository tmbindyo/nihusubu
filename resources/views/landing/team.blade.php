@extends('landing.layouts.app')

@section('title', 'Team')

@section('css')
        <!-- Web Fonts -->
        <link href="https://fonts.googleapis.com/css?family=Lato:300,400,400i|Montserrat:400,700" rel="stylesheet">

        <!-- Vendor Styles -->
        <link href="{{ asset('landing') }}/vendor/bootstrap/css/bootstrap.min.css" rel="stylesheet" type="text/css"/>
        <link href="{{ asset('landing') }}/css/animate.css" rel="stylesheet" type="text/css"/>
        <link href="{{ asset('landing') }}/vendor/themify/themify.css" rel="stylesheet" type="text/css"/>
        <link href="{{ asset('landing') }}/vendor/scrollbar/scrollbar.min.css" rel="stylesheet" type="text/css"/>

        <!-- Theme Styles -->
        <link href="{{ asset('landing') }}/css/style.css" rel="stylesheet" type="text/css"/>
        <link href="{{ asset('landing') }}/css/global/global.css" rel="stylesheet" type="text/css"/>

        <!-- Favicon -->
        <link rel="shortcut icon" href="{{ asset('') }}/nihusubu.ico" type="image/x-icon">
        <link rel="apple-touch-icon" href="{{ asset('landing') }}/img/apple-touch-icon.png">

@endsection
@section('content')
        <!--========== PROMO BLOCK ==========-->
        <div class="g-bg-position--center js__parallax-window" style="background: url({{ asset('landing') }}/img/1920x1080/09.jpg) 50% 0 no-repeat fixed;">
            <div class="g-container--md g-text-center--xs g-padding-y-150--xs">
                <p class="text-uppercase g-font-size-14--xs g-font-weight--700 g-color--white-opacity g-letter-spacing--2 g-margin-b-25--xs">30 years experience</p>
                <h1 class="g-font-size-40--xs g-font-size-50--sm g-font-size-60--md g-color--white g-letter-spacing--1">Creative Team</h1>
            </div>
        </div>
        <!--========== END PROMO BLOCK ==========-->

        <!--========== PAGE CONTENT ==========-->
        <!-- Speakers -->
        <div class="container g-padding-y-80--xs g-padding-y-125--sm">
            <div class="row g-overflow--hidden">
                <div class="col-xs-6 g-full-width--xs g-margin-b-30--xs g-margin-b-0--lg">
                    <!-- Speaker -->
                    <div class="center-block g-box-shadow__dark-lightest-v1 g-width-100-percent--xs g-width-400--lg">
                        <img class="img-responsive g-width-100-percent--xs" src="{{ asset('landing') }}/img/400x400/02.jpg" alt="Image">
                        <div class="g-position--overlay g-padding-x-30--xs g-padding-y-30--xs g-margin-t-o-60--xs">
                            <div class="g-bg-color--primary g-padding-x-15--xs g-padding-y-10--xs g-margin-b-20--xs">
                                <h4 class="g-font-size-22--xs g-font-size-26--sm g-color--white g-margin-b-0--xs">Anna Kusaikina</h4>
                            </div>
                            <p class="g-font-weight--700">Founder</p>
                            <p>Now that we've aligned the details, it's time to get things mapped out and organized. This part is really crucial in keeping the project in line to completion.</p>
                        </div>
                    </div>
                    <!-- End Speaker -->
                </div>
                <div class="col-xs-6 g-full-width--xs">
                    <!-- Speaker -->
                    <div class="center-block g-box-shadow__dark-lightest-v1 g-width-100-percent--xs g-width-400--lg">
                        <img class="img-responsive g-width-100-percent--xs" src="{{ asset('landing') }}/img/400x400/01.jpg" alt="Image">
                        <div class="g-position--overlay g-padding-x-30--xs g-padding-y-30--xs g-margin-t-o-60--xs">
                            <div class="g-bg-color--primary g-padding-x-15--xs g-padding-y-10--xs g-margin-b-20--xs">
                                <h4 class="g-font-size-22--xs g-font-size-26--sm g-color--white g-margin-b-0--xs">Lucas Richardson</h4>
                            </div>
                            <p class="g-font-weight--700">CEO</p>
                            <p>Now that we've aligned the details, it's time to get things mapped out and organized. This part is really crucial in keeping the project in line to completion.</p>
                        </div>
                    </div>
                    <!-- End Speaker -->
                </div>
            </div>
        </div>
        <!-- End Speakers -->

        <!-- Team -->
        <div class="row g-row-col--0">
            <div class="col-md-3 col-xs-6 g-full-width--xs">
                <div class="wow fadeInUp" data-wow-duration=".3" data-wow-delay=".1s">
                    <!-- Team -->
                    <div class="s-team-v1">
                        <img class="img-responsive g-width-100-percent--xs" src="{{ asset('landing') }}/img/400x400/03.jpg" alt="Image">
                        <div class="g-text-center--xs g-bg-color--white g-padding-x-30--xs g-padding-y-40--xs">
                            <h2 class="g-font-size-18--xs g-margin-b-5--xs">Jack Daniels</h2>
                            <span class="g-font-size-15--xs g-color--text"><i>Cardiology</i></span>
                        </div>
                    </div>
                    <!-- End Team -->
                </div>
            </div>
            <div class="col-md-3 col-xs-6 g-full-width--xs">
                <div class="wow fadeInUp" data-wow-duration=".3" data-wow-delay=".2s">
                    <!-- Team -->
                    <div class="s-team-v1">
                        <img class="img-responsive g-width-100-percent--xs" src="{{ asset('landing') }}/img/400x400/04.jpg" alt="Image">
                        <div class="g-text-center--xs g-bg-color--white g-padding-x-30--xs g-padding-y-40--xs">
                            <h3 class="g-font-size-18--xs g-margin-b-5--xs">Anna Kusaikina</h3>
                            <span class="g-font-size-15--xs g-color--text"><i>Pulmonology</i></span>
                        </div>
                    </div>
                    <!-- End Team -->
                </div>
            </div>
            <div class="col-md-3 col-xs-6 g-full-width--xs">
                <div class="wow fadeInUp" data-wow-duration=".3" data-wow-delay=".3s">
                    <!-- Team -->
                    <div class="s-team-v1">
                        <img class="img-responsive g-width-100-percent--xs" src="{{ asset('landing') }}/img/400x400/05.jpg" alt="Image">
                        <div class="g-text-center--xs g-bg-color--white g-padding-x-30--xs g-padding-y-40--xs">
                            <h4 class="g-font-size-18--xs g-margin-b-5--xs">Lucas Richardson</h4>
                            <span class="g-font-size-15--xs g-color--text"><i>Dental</i></span>
                        </div>
                    </div>
                    <!-- End Team -->
                </div>
            </div>
            <div class="col-md-3 col-xs-6 g-full-width--xs">
                <div class="wow fadeInUp" data-wow-duration=".3" data-wow-delay=".4s">
                    <!-- Team -->
                    <div class="s-team-v1">
                        <img class="img-responsive g-width-100-percent--xs" src="{{ asset('landing') }}/img/400x400/06.jpg" alt="Image">
                        <div class="g-text-center--xs g-bg-color--white g-padding-x-30--xs g-padding-y-40--xs">
                            <h4 class="g-font-size-18--xs g-margin-b-5--xs">Kira Doe</h4>
                            <span class="g-font-size-15--xs g-color--text"><i>Gynecology</i></span>
                        </div>
                    </div>
                    <!-- End Team -->
                </div>
            </div>
        </div>
        <!-- End Team -->

        <!-- Feedback Form -->
        <div class="g-position--relative g-bg-color--dark-light">
            <div class="g-container--md g-padding-y-80--xs g-padding-y-125--sm">
                <div class="g-text-center--xs g-margin-b-80--xs">
                    <p class="text-uppercase g-font-size-14--xs g-font-weight--700 g-color--white-opacity g-letter-spacing--2 g-margin-b-25--xs">Contact Us</p>
                    <h2 class="g-font-size-32--xs g-font-size-36--md g-color--white">Get in Touch</h2>
                </div>
                <div class="row g-row-col--5 g-margin-b-80--xs">
                    <div class="col-xs-4 g-full-width--xs g-margin-b-50--xs g-margin-b-0--sm">
                        <div class="g-text-center--xs">
                            <i class="g-display-block--xs g-font-size-40--xs g-color--white-opacity g-margin-b-30--xs ti-email"></i>
                            <h4 class="g-font-size-18--xs g-color--white g-margin-b-5--xs">Email</h4>
                            <p class="g-color--white-opacity">support@keenthemes.com</p>
                        </div>
                    </div>
                    <div class="col-xs-4 g-full-width--xs g-margin-b-50--xs g-margin-b-0--sm">
                        <div class="g-text-center--xs">
                            <i class="g-display-block--xs g-font-size-40--xs g-color--white-opacity g-margin-b-30--xs ti-map-alt"></i>
                            <h4 class="g-font-size-18--xs g-color--white g-margin-b-5--xs">Address</h4>
                            <p class="g-color--white-opacity">277 Bedford Avenue, Brooklyn</p>
                        </div>
                    </div>
                    <div class="col-xs-4 g-full-width--xs">
                        <div class="g-text-center--xs">
                            <i class="g-display-block--xs g-font-size-40--xs g-color--white-opacity g-margin-b-30--xs ti-headphone-alt"></i>
                            <h4 class="g-font-size-18--xs g-color--white g-margin-b-5--xs">Call at</h4>
                            <p class="g-color--white-opacity">+ (1) 001 389 3720</p>
                        </div>
                    </div>
                </div>
                <form class="center-block g-width-500--sm g-width-550--md">
                    <div class="g-margin-b-30--xs">
                        <input type="text" class="form-control s-form-v3__input" placeholder="* Name">
                    </div>
                    <div class="row g-row-col-5 g-margin-b-50--xs">
                        <div class="col-sm-6 g-margin-b-30--xs g-margin-b-0--md">
                            <input type="email" class="form-control s-form-v3__input" placeholder="* Email">
                        </div>
                        <div class="col-sm-6">
                            <input type="text" class="form-control s-form-v3__input" placeholder="* Phone">
                        </div>
                    </div>
                    <div class="g-margin-b-80--xs">
                        <textarea class="form-control s-form-v3__input" rows="5" placeholder="* Your message"></textarea>
                    </div>
                    <div class="g-text-center--xs">
                        <button type="submit" class="text-uppercase s-btn s-btn--md s-btn--white-bg g-radius--50 g-padding-x-70--xs g-margin-b-20--xs">Submit</button>
                    </div>
                </form>
            </div>
            <img class="s-mockup-v2" src="{{ asset('landing') }}/img/mockups/pencil-01.png" alt="Mockup Image">
        </div>
        <!-- End Feedback Form -->
        <!--========== END PAGE CONTENT ==========-->
@endsection

@section('js')

    <!-- Back To Top -->
    <a href="javascript:void(0);" class="s-back-to-top js__back-to-top"></a>

    <!--========== JAVASCRIPTS (Load javascripts at bottom, this will reduce page load time) ==========-->
    <!-- Vendor -->
    <script type="text/javascript" src="{{ asset('landing') }}/vendor/jquery.min.js"></script>
    <script type="text/javascript" src="{{ asset('landing') }}/vendor/jquery.migrate.min.js"></script>
    <script type="text/javascript" src="{{ asset('landing') }}/vendor/bootstrap/js/bootstrap.min.js"></script>
    <script type="text/javascript" src="{{ asset('landing') }}/vendor/jquery.smooth-scroll.min.js"></script>
    <script type="text/javascript" src="{{ asset('landing') }}/vendor/jquery.back-to-top.min.js"></script>
    <script type="text/javascript" src="{{ asset('landing') }}/vendor/scrollbar/jquery.scrollbar.min.js"></script>
    <script type="text/javascript" src="{{ asset('landing') }}/vendor/jquery.parallax.min.js"></script>
    <script type="text/javascript" src="{{ asset('landing') }}/vendor/jquery.wow.min.js"></script>

    <!-- General Components and Settings -->
    <script type="text/javascript" src="{{ asset('landing') }}/js/global.min.js"></script>
    <script type="text/javascript" src="{{ asset('landing') }}/js/components/header-sticky.min.js"></script>
    <script type="text/javascript" src="{{ asset('landing') }}/js/components/scrollbar.min.js"></script>
    <script type="text/javascript" src="{{ asset('landing') }}/js/components/wow.min.js"></script>
    <!--========== END JAVASCRIPTS ==========-->

@endsection
